"""
Módulo de preprocesamiento de datos para clusterización
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Tuple


# Lista de columnas esperadas en el output final (175 columnas + Cluster = 176 total)
EXPECTED_COLUMNS = [
    "IdUnico", "Fecha_Ingreso", "Nombre_Estado", "Nombre_Tipo_Vinculacion", "Estado_Civil",
    "Personas_a_Cargo", "Personas_a_Cargo_Menores_18", "Sexo", "Estrato", "Nombre_Tipo_Vivienda",
    "Nombre_Nivel_Academico", "Fecha_Nacimiento", "Ingresos", "Nombre_Titulo_Obtenido",
    "Nombre_Ocupacion", "Saldo_aportes", "Cuotas_canceladas_aportes", "Cuotas_mora_aportes",
    "Vlr_mora", "Ingresos_Deflactados", "Zona", "Cta_Dep", "Cta_Juve", "Fondo_Soc", "Cheque_Cta",
    "Cupo_Activ", "Tarj_Debit", "Cdat", "PAP", "Creditos", "Cred_Vivienda", "Cred_Lib_Inv_con_Garant",
    "Cred_Lib_Inv_sin_Garant", "Cred_Vehic", "Cred_Creac_Empr", "Cred_Educac", "Cred_Otros", "Pila",
    "bancaseguro", "AFC", "TieneVISA", "saldo_VISA", "CuotaManejo", "Microcreditos", "Credisolidario",
    "Solidaridad", "Exequial", "Herencia", "Hospitalizacion", "Recuperacion", "Solvencia", "Tranquilidad",
    "Vida", "VidaClasica", "Seguros2", "SeguroAuto", "SeguroSinAuto", "HogarMasyTotalHome", "Soat",
    "TotalRCMedica", "OtrasPolizas", "MI", "CEM", "SAOR", "MPT", "numedad", "PlanEducativo",
    "MasterCardCupo", "MasterCardSaldo", "Tarjetas", "Credimutual", "SolidaridadPBI", "Libranza",
    "ReestructuracionConsumo", "COERotativo", "Originadores", "COE", "CupoEducar", "CreditoTurismo",
    "CreditoSaludBienestar", "ReestructuracionComercial", "ReestructuracionVivienda", "CreditoCapitaldeTrabajo",
    "Findeter", "Bancoldex", "Sobregiro", "CreditoCalamidad", "CreditoProductivo", "FindeterRotativo",
    "NominaFacil", "PagodeObligaciones", "Desempleo", "FondoSocialViviendaPatrimonial", "FondoSocialViviendaVida",
    "numCantidadProductos", "FondoSocialViviendaBanco", "PrimaNivelada", "Crediasociado", "CuentaPension",
    "FIC_365", "FIC_90", "FIC_Vista", "Inversiones_No_Tradicionales", "Renta_Fija_Corto_Plazo",
    "log_ingresos", "log_ingresos_deflactados", "Antiguedad_dias", "Edad", "Area_Titulo", "Region",
    "Nombre_Estado_Activo Normal", "Nombre_Estado_Inactivo", "Nombre_Estado_Receso",
    "Nombre_Estado_Suspendido Cobranza Interna", "Nombre_Estado_Suspendido Fallecido",
    "Nombre_Estado_Suspendido Normal",
    "Nombre_Tipo_Vinculacion_Empleado No Profesional", "Nombre_Tipo_Vinculacion_Empresa Persona Natural",
    "Nombre_Tipo_Vinculacion_Estudiante", "Nombre_Tipo_Vinculacion_Familiar Asociado",
    "Nombre_Tipo_Vinculacion_Familiar Asociado Fallecido", "Nombre_Tipo_Vinculacion_Mayor 60",
    "Nombre_Tipo_Vinculacion_Personas Jurídicas", "Nombre_Tipo_Vinculacion_Profesional",
    "Nombre_Tipo_Vinculacion_Recién Graduado", "Nombre_Tipo_Vinculacion_Transición",
    "Nombre_Tipo_Vinculacion_Técnicos y Tecnólogos", "Estado_Civil_Divorciado", "Estado_Civil_No Cruza",
    "Estado_Civil_No Definido", "Estado_Civil_Separado", "Estado_Civil_Soltero", "Estado_Civil_Union Libre",
    "Estado_Civil_Viudo", "Sexo_J", "Sexo_M", "Estrato_2", "Estrato_3", "Estrato_4", "Estrato_5",
    "Estrato_6", "Estrato_9", "Estrato_No Cruza", "Nombre_Tipo_Vivienda_Desconocida",
    "Nombre_Tipo_Vivienda_Familiar", "Nombre_Tipo_Vivienda_No Cruza", "Nombre_Tipo_Vivienda_Propia",
    "Nombre_Nivel_Academico_Ninguno", "Nombre_Nivel_Academico_No Cruza", "Nombre_Nivel_Academico_Otros",
    "Nombre_Nivel_Academico_Profesional", "Nombre_Nivel_Academico_Tecnólogo", "Nombre_Nivel_Academico_Técnico",
    "Nombre_Ocupacion_Asalariado", "Nombre_Ocupacion_Estudiante", "Nombre_Ocupacion_Independiente",
    "Nombre_Ocupacion_Ninguno / No definido", "Nombre_Ocupacion_No Cruza", "Nombre_Ocupacion_Otro tipo de Actividad",
    "Nombre_Ocupacion_Pensionado - Jubilado", "Nombre_Ocupacion_Rentista Capital", "Nombre_Ocupacion_Socio Sociedad",
    "Andina", "Caribe", "Orinoquía", "Otro", "Pacífica", "Arquitectura", "Ciencias Sociales", "Comunicaciones",
    "Educación", "Ingeniería", "Otro.1", "Salud", "Tecnología"
]


class DataPreprocessor:
    """Clase para manejar todo el preprocesamiento de datos"""
    
    def __init__(self, fecha_referencia: str = None):
        """
        Inicializa el preprocesador con las columnas a eliminar
        
        Args:
            fecha_referencia: Fecha de referencia para calcular Antiguedad_dias y Edad.
                            Formato: 'YYYY-MM-DD'. Si es None, usa la fecha actual.
                            IMPORTANTE: Debe coincidir con la fecha usada al entrenar los modelos.
        """
        # Fecha de referencia para cálculos de antigüedad y edad
        if fecha_referencia:
            self.fecha_referencia = pd.Timestamp(fecha_referencia)
        else:
            # Usar fecha actual (today)
            self.fecha_referencia = pd.Timestamp.today()
        
        # Columnas a eliminar inicialmente (las que tienen versión con "Nombre_" se mantienen)
        self.columnas_a_eliminar_inicial = [
            # Columnas que tienen una versión "Nombre_" (mantener la versión "Nombre_")
            'Estado',              # Mantener Nombre_Estado
            'Tipo_Vinculacion',    # Mantener Nombre_Tipo_Vinculacion
            'Tipo_Vivienda',       # Mantener Nombre_Tipo_Vivienda
            'Nivel_Academico',     # Mantener Nombre_Nivel_Academico
            'Ocupacion',           # Mantener Nombre_Ocupacion
            
            # Columnas no usadas en el modelo
            'Motivo_Retiro',
            'Segmento_Consumo',
            'Segmento_Rotativo',
            'Segmento_Ciclo_de_Vida',
            'Segmento_Ingresos_vs_Antiguedad',
            'Descripcion_Oficina',
            'Regional',
            'Fecha_Ingresos',
            'Fecha_Ingresos_Deflactados',
            'indInactivo',
            'Ptaje_acierta',
        ]
        
        # Columnas que deben eliminarse porque no se usan en el modelo final
        # IMPORTANTE: NO eliminar columnas que aparecen en EXPECTED_COLUMNS
        self.columns_to_drop_detailed = [
            'IdUnico',  # Se guarda aparte para el output
            'Personas_a_Cargo_Menores_18', 'PAP', 'Pila', 'bancaseguro', 'AFC',
            'TieneVISA', 'Credisolidario',
            'Exequial', 'Herencia', 'Hospitalizacion', 'Recuperacion', 'Tranquilidad', 'Vida',
            'VidaClasica', 'HogarMasyTotalHome', 'MI', 'CEM', 'SAOR', 'MPT',
            'PlanEducativo',
            'Credimutual', 'SolidaridadPBI', 'Libranza', 'ReestructuracionConsumo', 'COERotativo',
            'Originadores', 'COE', 'CupoEducar', 'CreditoTurismo',
            'CreditoSaludBienestar', 'ReestructuracionComercial', 'ReestructuracionVivienda',
            'Findeter', 'Bancoldex', 'Sobregiro', 'FindeterRotativo', 'NominaFacil', 'Desempleo',
            'FondoSocialViviendaPatrimonial', 'FondoSocialViviendaBanco', 'PrimaNivelada', 'FIC_365',
            'FIC_90', 'FIC_Vista', 'Inversiones_No_Tradicionales',
            "Inversiones_No_Tradicionales",
            "Renta_Fija_Corto_Plazo",
            "CuentaPension",
            "FondoSocialViviendaVida",
            "PagodeObligaciones",
            "CreditoProductivo",
            "CreditoCalamidad",
            "CreditoCapitaldeTrabajo",
            "Microcreditos",
            "CuotaManejo",
            "Cred_Otros",
            "Cred_Creac_Empr",
            "Cred_Lib_Inv_con_Garant"
        ]
        
        self.region_map = {
            # Región Andina
            "Bogotá": "Andina", "Medellín": "Andina", "Manizales": "Andina",
            "Pereira": "Andina", "Ibagué": "Andina", "Tunja": "Andina",
            "Armenia": "Andina", "Neiva": "Andina", "Bucaramanga": "Andina",
            "Cúcuta": "Andina", "Popayán": "Andina", "Pasto": "Andina",
            "Chía": "Andina", "Zipaquirá": "Andina", "Soacha": "Andina",
            "Floridablanca": "Andina", "Girón": "Andina", "Dosquebradas": "Andina",
            # Región Caribe
            "Barranquilla": "Caribe", "Cartagena": "Caribe", "Santa Marta": "Caribe",
            "Montería": "Caribe", "Sincelejo": "Caribe", "Valledupar": "Caribe",
            "Riohacha": "Caribe", "Ciénaga": "Caribe", "Soledad": "Caribe",
            "Malambo": "Caribe", "Sabanalarga": "Caribe", "Turbaco": "Caribe",
            "Magangué": "Caribe", "Lorica": "Caribe", "Plato": "Caribe",
            "Cereté": "Caribe",
            # Región Pacífica
            "Cali": "Pacífica", "Buenaventura": "Pacífica", "Quibdó": "Pacífica",
            "Tumaco": "Pacífica", "Guapi": "Pacífica", "Timbiquí": "Pacífica",
            "Istmina": "Pacífica", "San Andrés de Tumaco": "Pacífica",
            # Región Orinoquía
            "Villavicencio": "Orinoquía", "Yopal": "Orinoquía", "Arauca": "Orinoquía",
            "Puerto Carreño": "Orinoquía", "Tame": "Orinoquía", "Paz de Ariporo": "Orinoquía",
            "Saravena": "Orinoquía",
            # Región Amazonía
            "Leticia": "Amazonía", "Florencia": "Amazonía", "Mocoa": "Amazonía",
            "San José del Guaviare": "Amazonía", "Mitú": "Amazonía", "Inírida": "Amazonía",
            "Puerto Asís": "Amazonía", "La Chorrera": "Amazonía",
        }
    
    def agrupar_titulo(self, titulo: str) -> str:
        """Agrupa títulos académicos en categorías"""
        titulo = str(titulo).lower()
        
        if "enfermer" in titulo or "quirúrgica" in titulo or "medicina" in titulo:
            return "Salud"
        elif "sistem" in titulo or "analisis" in titulo or "tecnolog" in titulo:
            return "Tecnología"
        elif "admin" in titulo or "negocios" in titulo or "gestion" in titulo:
            return "Administración"
        elif "derecho" in titulo or "relaciones internacionales" in titulo or "ciencias sociales" in titulo:
            return "Ciencias Sociales"
        elif "docente" in titulo or "lic." in titulo:
            return "Educación"
        elif "ingenier" in titulo:
            return "Ingeniería"
        elif "comunicacion" in titulo or "periodismo" in titulo:
            return "Comunicaciones"
        elif "arquitectura" in titulo:
            return "Arquitectura"
        else:
            return "Otro"
    
    def mapear_region(self, zona: str) -> str:
        """Mapea zona a región"""
        zona = zona.strip().title()
        return self.region_map.get(zona, "Otro")
    
    def process(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Procesa el DataFrame completo EXACTAMENTE como el notebook
        
        Args:
            df: DataFrame con los datos crudos
            
        Returns:
            Tuple con (DataFrame procesado con TODAS las columnas, Series con IdUnico)
        """
        # Guardar IdUnico y otras columnas de texto ANTES de cualquier procesamiento
        columnas_texto_guardar = ['IdUnico', 'Fecha_Ingreso', 'Nombre_Estado', 'Nombre_Tipo_Vinculacion', 
                                  'Estado_Civil', 'Sexo', 'Nombre_Tipo_Vivienda', 'Nombre_Nivel_Academico',
                                  'Fecha_Nacimiento', 'Nombre_Titulo_Obtenido', 'Nombre_Ocupacion', 'Zona']
        
        df_texto_original = df[[col for col in columnas_texto_guardar if col in df.columns]].copy()
        id_unico = df['IdUnico'].copy() if 'IdUnico' in df.columns else None
        
        # 1. Eliminar columnas redundantes iniciales (las que NO tienen prefijo "Nombre_")
        df = df.drop(columns=self.columnas_a_eliminar_inicial, errors='ignore')
        
        # 2. Eliminar Egresos
        df = df.drop(columns=['Egresos'], errors='ignore')
        
        # 3. Eliminar filas con valores nulos en columnas críticas
        indices_validos = df.dropna(subset=[
            'Saldo_aportes', 'Cuotas_canceladas_aportes', 'Cuotas_mora_aportes', 
            'Vlr_mora', 'Ingresos'
        ], how='any').index
        
        df = df.loc[indices_validos]
        
        # Actualizar id_unico para que solo incluya las filas válidas
        if id_unico is not None:
            id_unico = id_unico.loc[indices_validos]
        
        # Actualizar df_texto_original para que solo incluya las filas válidas
        df_texto_original = df_texto_original.loc[indices_validos]
        
        # 4. Crear variables logarítmicas ANTES de eliminar columnas
        # IMPORTANTE: Solo calcular si NO existen ya en el DataFrame de entrada
        # (el notebook original puede ya tener estos valores con una transformación específica)
        if 'log_ingresos' in df.columns:
            print(f"⚠️ log_ingresos YA EXISTE en df, preservando valores existentes")
            print(f"  Valores: {df['log_ingresos'].head(3).tolist()}")
        elif 'Ingresos' in df.columns:
            print(f"ℹ️ Calculando log_ingresos desde Ingresos")
            df['log_ingresos'] = np.log(df['Ingresos'].replace(0, np.nan))
        
        if 'log_ingresos_deflactados' in df.columns:
            print(f"⚠️ log_ingresos_deflactados YA EXISTE en df, preservando valores existentes")
            print(f"  Valores: {df['log_ingresos_deflactados'].head(3).tolist()}")
        elif 'Ingresos_Deflactados' in df.columns:
            print(f"ℹ️ Calculando log_ingresos_deflactados desde Ingresos_Deflactados")
            df['log_ingresos_deflactados'] = np.log(df['Ingresos_Deflactados'].replace(0, np.nan))
        
        # 5. Eliminar columnas detalladas
        df = df.drop(columns=self.columns_to_drop_detailed, errors='ignore')
        
        # 6. Procesar fechas y crear variables derivadas
        if 'Fecha_Ingreso' in df.columns:
            df['Fecha_Ingreso'] = pd.to_datetime(df['Fecha_Ingreso'], format='%m/%d/%Y', errors='coerce')
            df['Antiguedad_dias'] = (self.fecha_referencia - df['Fecha_Ingreso']).dt.days
            # NO eliminar Fecha_Ingreso aquí, la mantenemos para el output
        
        if 'Fecha_Nacimiento' in df.columns:
            df['Fecha_Nacimiento'] = pd.to_datetime(df['Fecha_Nacimiento'], format='%m/%d/%Y', errors='coerce')
            df['Edad'] = df['Fecha_Nacimiento'].apply(
                lambda fecha: self.fecha_referencia.year - fecha.year - (
                    (self.fecha_referencia.month, self.fecha_referencia.day) < (fecha.month, fecha.day)
                )
                if pd.notna(fecha) else np.nan
            )
            # NO eliminar Fecha_Nacimiento aquí, la mantenemos para el output
        
        # 7. Procesar variables categóricas
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Remover columnas especiales de la lista de categóricas
        if 'Nombre_Titulo_Obtenido' in cat_cols:
            cat_cols.remove('Nombre_Titulo_Obtenido')
        if 'Zona' in cat_cols:
            cat_cols.remove('Zona')
        
        # 8. Procesar título académico
        if 'Nombre_Titulo_Obtenido' in df.columns:
            df['Area_Titulo'] = df['Nombre_Titulo_Obtenido'].apply(self.agrupar_titulo)
            # Keep all dummy columns to match the notebook output
            df_dummies_titulo = pd.get_dummies(df['Area_Titulo'], drop_first=False)
            # Agregar Area_Titulo al dataframe de texto
            df_texto_original['Area_Titulo'] = df['Area_Titulo']
        else:
            df_dummies_titulo = pd.DataFrame()
        
        # 9. Procesar zona/región
        if 'Zona' in df.columns:
            df['Region'] = df['Zona'].apply(self.mapear_region)
            # Keep all dummy columns to match the notebook output
            df_dummies_region = pd.get_dummies(df['Region'], drop_first=False)
            # Agregar Region al dataframe de texto
            df_texto_original['Region'] = df['Region']
        else:
            df_dummies_region = pd.DataFrame()
        
        # 10. One-hot encoding de categóricas restantes
        if cat_cols:
            # Keep all dummy columns (drop_first=False) to preserve the same
            # encoding as the original notebook/output
            df_dummies = pd.get_dummies(df[cat_cols], drop_first=False, prefix_sep='_')
        else:
            df_dummies = pd.DataFrame()
        
        # 11. Eliminar columnas categóricas ANTES de concatenar para evitar duplicados
        # Solo eliminar 'Nombre_Titulo_Obtenido' y 'Zona' porque ya tenemos Area_Titulo y Region
        columns_to_drop_before_concat = ['Nombre_Titulo_Obtenido', 'Zona', 'Area_Titulo', 'Region']
        columns_to_drop_before_concat.extend(cat_cols)  # Añadir todas las categóricas
        df = df.drop(columns=columns_to_drop_before_concat, errors='ignore')
        
        # 12. Concatenar dummies (mantener Area_Titulo y Region en el DataFrame final)
        df = pd.concat([df, df_dummies, df_dummies_region, df_dummies_titulo], axis=1)
        
        # 13. Verificar y eliminar columnas duplicadas antes de reindexar
        if df.columns.duplicated().any():
            duplicated_cols = df.columns[df.columns.duplicated()].tolist()
            print(f"⚠️ Columnas duplicadas detectadas: {duplicated_cols}")
            # Mantener solo la primera ocurrencia de cada columna
            df = df.loc[:, ~df.columns.duplicated()]
        
        # 14. Reindexar SOLO las columnas numéricas para el modelo
        # Las columnas que falten se rellenarán con 0 (como float64)
        df_numerico = df.reindex(columns=EXPECTED_COLUMNS, fill_value=0.0)
        
        # 15. Asegurar que las columnas numéricas sean float64
        for col in df_numerico.columns:
            # Saltar columnas que están en df_texto_original
            if col in df_texto_original.columns:
                continue
            if col != 'Cluster':
                # Solo convertir columnas numéricas
                try:
                    df_numerico[col] = pd.to_numeric(df_numerico[col], errors='coerce').astype(np.float64)
                except (ValueError, TypeError):
                    pass  # Dejar como está si no se puede convertir
        
        # 16. Reemplazar las columnas de texto en df_numerico con las originales guardadas
        for col in df_texto_original.columns:
            if col in df_numerico.columns:
                df_numerico[col] = df_texto_original[col]
        
        return df_numerico, id_unico

