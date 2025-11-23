"""
Router para endpoints de clustering
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import numpy as np
import io
import logging
from typing import Optional

from app.preprocessing import DataPreprocessor
from app.prediction import get_clustering_model

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/cluster")
async def cluster_users(
    file: UploadFile = File(..., description="Archivo CSV o XLSX con datos de usuarios")
):
    """
    Endpoint para clusterizar usuarios
    
    Args:
        file: Archivo CSV o XLSX con datos de usuarios
        
    Returns:
        Archivo CSV con los datos originales más la columna 'Cluster'
    """
    try:
        # Validar tipo de archivo
        filename = file.filename.lower()
        if not (filename.endswith('.csv') or filename.endswith('.xlsx')):
            raise HTTPException(
                status_code=400,
                detail="Formato de archivo no soportado. Use CSV o XLSX"
            )
        
        # Leer archivo
        contents = await file.read()
        
        if filename.endswith('.csv'):
            df_original = pd.read_csv(io.BytesIO(contents))
        else:
            df_original = pd.read_excel(io.BytesIO(contents))
        
        logger.info(f"Archivo recibido: {file.filename}, filas: {len(df_original)}")
        
        # Preprocesar datos
        preprocessor = DataPreprocessor()
        df_processed, _ = preprocessor.process(df_original.copy())
        
        logger.info(f"Datos preprocesados: {len(df_processed)} filas")
        
        # Obtener predicciones
        model = get_clustering_model()
        labels, _, df_completo = model.predict(df_processed)
        
        # Usar df_completo que ya tiene todas las transformaciones aplicadas
        df_result = df_completo.copy()
        
        # Resetear índices
        df_result = df_result.reset_index(drop=True)
        
        # Agregar columna Cluster
        df_result['Cluster'] = labels
        
        # Convertir columnas one-hot de float64 a bool
        # Identificar columnas one-hot por sus nombres y tipos
        onehot_columns = [col for col in df_result.columns if any(
            col.startswith(prefix) for prefix in [
                'Nombre_Estado_', 'Nombre_Tipo_Vinculacion_', 'Estado_Civil_',
                'Sexo_', 'Estrato_', 'Nombre_Tipo_Vivienda_', 'Nombre_Nivel_Academico_',
                'Nombre_Ocupacion_', 'Andina', 'Caribe', 'Orinoquía', 'Otro', 'Pacífica',
                'Arquitectura', 'Ciencias Sociales', 'Comunicaciones', 'Educación',
                'Ingeniería', 'Salud', 'Tecnología'
            ]
        )]
        
        for col in onehot_columns:
            if col in df_result.columns and df_result[col].dtype in [np.float64, np.float32, float]:
                # Convertir float64 (0.0, 1.0) a bool (False, True)
                df_result[col] = df_result[col].astype(bool)
        
        # Convertir fechas a formato compatible con Supabase (YYYY-MM-DD)
        if 'Fecha_Ingreso' in df_result.columns:
            df_result['Fecha_Ingreso'] = pd.to_datetime(df_result['Fecha_Ingreso']).dt.strftime('%Y-%m-%d')
        if 'Fecha_Nacimiento' in df_result.columns:
            df_result['Fecha_Nacimiento'] = pd.to_datetime(df_result['Fecha_Nacimiento']).dt.strftime('%Y-%m-%d')
        
        # Convertir IdUnico y Cluster a texto
        if 'IdUnico' in df_result.columns:
            df_result['IdUnico'] = df_result['IdUnico'].astype(str)
        if 'Cluster' in df_result.columns:
            df_result['Cluster'] = df_result['Cluster'].astype(str)
        
        logger.info(f"Clusterización completada. Clusters encontrados: {df_result['Cluster'].nunique()}")
        
        # Normalizar nombres de columnas para compatibilidad con Supabase
        # Convertir a minúsculas, reemplazar espacios por guiones bajos, eliminar caracteres especiales
        df_result.columns = (
            df_result.columns
            .str.lower()  # Minúsculas
            .str.replace(' ', '_', regex=False)  # Espacios a guiones bajos
            .str.replace('/', '_', regex=False)  # Slashes a guiones bajos
            .str.replace('-', '_', regex=False)  # Guiones a guiones bajos
            .str.replace('ó', 'o', regex=False)  # Acentos
            .str.replace('í', 'i', regex=False)
            .str.replace('á', 'a', regex=False)
            .str.replace('é', 'e', regex=False)
            .str.replace('ú', 'u', regex=False)
            .str.replace('ñ', 'n', regex=False)
            .str.replace('___', '_', regex=False)  # Triple guion bajo a uno
            .str.replace('__', '_', regex=False)  # Doble guion bajo a uno
        )
        
        # Ajustes específicos para nombres que no coinciden exactamente
        column_mapping = {
            'otro.1': 'otro_1',
            'nombre_ocupacion_ninguno___no_definido': 'nombre_ocupacion_ninguno_no_definido',
            'nombre_estado_activo_normal': 'nombre_estado_activo_normal',
            'nombre_estado_suspendido_cobranza_interna': 'nombre_estado_suspendido_cobranza_interna',
            'nombre_tipo_vinculacion_tecnicos_y_tecnologos': 'nombre_tipo_vinculacion_tecnicos_y_tecnologos',
            'nombre_tipo_vinculacion_recien_graduado': 'nombre_tipo_vinculacion_recien_graduado',
            'nombre_nivel_academico_tecnologo': 'nombre_nivel_academico_tecnologo',
            'nombre_nivel_academico_tecnico': 'nombre_nivel_academico_tecnico',
            'nombre_ocupacion_pensionado___jubilado': 'nombre_ocupacion_pensionado_jubilado',
            'orinoquia': 'orinoquia'
        }
        
        df_result.rename(columns=column_mapping, inplace=True)
        
        logger.info(f"Columnas normalizadas: {list(df_result.columns)}")
        
        # Convertir columnas booleanas que son productos/servicios
        # Estas columnas deben ser boolean en Supabase
        boolean_columns = [
            'cta_dep', 'cta_juve', 'fondo_soc', 'cheque_cta', 'cupo_activ', 'tarj_debit',
            'cdat', 'pap', 'creditos', 'cred_vivienda', 'cred_lib_inv_con_garant',
            'cred_lib_inv_sin_garant', 'cred_vehic', 'cred_creac_empr', 'cred_educac',
            'cred_otros', 'pila', 'bancaseguro', 'afc', 'tienevisa', 'microcreditos',
            'credisolidario', 'solidaridad', 'exequial', 'herencia', 'hospitalizacion',
            'recuperacion', 'solvencia', 'tranquilidad', 'vida', 'vidaclasica', 'seguros2',
            'seguroauto', 'segurosinauto', 'hogarmasytotalhome', 'soat', 'totalrcmedica',
            'otraspolizas', 'mi', 'cem', 'saor', 'mpt', 'planeducativo', 'tarjetas',
            'credimutual', 'solidaridadpbi', 'libranza', 'reestructuracionconsumo',
            'coerotativo', 'originadores', 'coe', 'cupoeducar', 'creditoturismo',
            'creditosaludbienestar', 'reestructuracioncomercial', 'reestructuracionvivienda',
            'creditocapitaldetrabajo', 'findeter', 'bancoldex', 'sobregiro',
            'creditocalamidad', 'creditoproductivo', 'findeterrotativo', 'nominafacil',
            'pagodeobligaciones', 'desempleo', 'fondosocialviviendapatrimonial',
            'fondosocialviviendavida', 'fondosocialviviendabanco', 'primanivelada',
            'crediasociado', 'cuentapension'
        ]
        
        # También incluir las columnas one-hot categóricas (después de normalización)
        categorical_boolean_columns = [col for col in df_result.columns if any(
            col.startswith(prefix) for prefix in [
                'nombre_estado_', 'nombre_tipo_vinculacion_', 'estado_civil_',
                'sexo_', 'estrato_', 'nombre_tipo_vivienda_', 'nombre_nivel_academico_',
                'nombre_ocupacion_', 'andina', 'caribe', 'orinoquia', 'otro', 'pacifica',
                'arquitectura', 'ciencias_sociales', 'comunicaciones', 'educacion',
                'ingenieria', 'salud', 'tecnologia'
            ]
        )]
        
        all_boolean_columns = list(set(boolean_columns + categorical_boolean_columns))
        
        # Convertir a boolean (True/False en lugar de 0.0/1.0)
        for col in all_boolean_columns:
            if col in df_result.columns:
                # Convertir a numérico primero, luego a int, luego a bool
                df_result[col] = pd.to_numeric(df_result[col], errors='coerce').fillna(0).astype(int).astype(bool)
        
        # Convertir columnas float que deberían ser int (compatibilidad con Supabase)
        # Estas son columnas pequeñas (booleanos, contadores, flags)
        small_int_columns = [
            'personas_a_cargo', 'personas_a_cargo_menores_18', 'cuotas_canceladas_aportes',
            'cuotas_mora_aportes', 'numedad', 'numcantidadproductos',
            'antiguedad_dias', 'edad', 'estrato'
        ]
        
        # Convertir a int las columnas pequeñas
        for col in small_int_columns:
            if col in df_result.columns:
                df_result[col] = pd.to_numeric(df_result[col], errors='coerce').fillna(0).astype(int)
        
        # Para columnas monetarias/grandes, convertir a int también (Supabase usa bigint)
        big_int_columns = [
            'ingresos', 'saldo_aportes', 'vlr_mora', 'ingresos_deflactados',
            'saldo_visa', 'cuotamanejo', 'mastercardcupo', 'mastercardsaldo',
            'fic_365', 'fic_90', 'fic_vista', 'inversiones_no_tradicionales',
            'renta_fija_corto_plazo'
        ]
        
        for col in big_int_columns:
            if col in df_result.columns:
                df_result[col] = pd.to_numeric(df_result[col], errors='coerce').fillna(0).astype(int)
        
        # Solo log_ingresos y log_ingresos_deflactados se mantienen como float
        float_columns = ['log_ingresos', 'log_ingresos_deflactados']
        
        for col in float_columns:
            if col in df_result.columns:
                df_result[col] = pd.to_numeric(df_result[col], errors='coerce').fillna(0)
        
        # Crear archivo CSV en memoria como bytes
        csv_buffer = io.BytesIO()
        
        # Guardar DataFrame como CSV en el buffer de bytes
        csv_string = df_result.to_csv(index=False, encoding='utf-8')
        csv_buffer.write(csv_string.encode('utf-8'))
        
        # Resetear puntero al inicio
        csv_buffer.seek(0)
        
        # Preparar respuesta como descarga binaria
        return StreamingResponse(
            csv_buffer,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": "attachment; filename=clustered_users.csv",
                "Content-Type": "application/octet-stream",
                "Accept-Ranges": "bytes"
            }
        )
        
    except ValueError as e:
        logger.error(f"Error de validación: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error procesando archivo: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando el archivo: {str(e)}"
        )


@router.get("/cluster/info")
async def get_cluster_info():
    """
    Obtiene información sobre el modelo de clustering
    
    Returns:
        Información del modelo
    """
    try:
        model = get_clustering_model()
        return {
            "status": "ready",
            "n_clusters": int(model.kmeans_model.n_clusters),
            "umap_components": int(model.umap_model.n_components),
            "models_loaded": {
                "umap": model.umap_model is not None,
                "kmeans": model.kmeans_model is not None,
                "scaler": model.scaler is not None
            }
        }
    except Exception as e:
        logger.error(f"Error obteniendo info del modelo: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo información del modelo: {str(e)}"
        )
