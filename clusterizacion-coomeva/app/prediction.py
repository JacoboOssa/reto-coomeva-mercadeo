"""
Módulo para cargar modelos y realizar predicciones
VERSIÓN FINAL - Sin usar UMAP en absoluto
"""
import logging
from typing import Tuple
from pathlib import Path
import numpy as np
import pandas as pd
import pickle

logger = logging.getLogger(__name__)


class ClusteringModel:
    """Clase para manejar la carga de modelos y predicciones"""

    def __init__(self, models_path: str = "models"):
        """
        Inicializa el modelo de clustering

        Args:
            models_path: Ruta a la carpeta de modelos
        """
        self.models_path = Path(models_path)
        self.kmeans_model = None
        self.scaler = None
        
        # Datos UMAP pre-calculados (reemplazan al modelo UMAP)
        self.umap_embeddings = None  # Coordenadas UMAP del entrenamiento
        self.knn_index = None        # Índice KNN para búsqueda rápida
        self.feature_names = None    # Nombres de features esperados
        
        self._load_models()

    def _load_models(self):
        """Carga los modelos desde archivos pickle"""
        try:
            logger.info("="*60)
            logger.info("INICIANDO CARGA DE MODELOS")
            logger.info("="*60)
            
            # 1. Cargar Scaler
            scaler_path = self.models_path / "scaler_model.pkl"
            logger.info(f"[1/3] Cargando Scaler desde {scaler_path}...")
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            logger.info(f"  ✓ Scaler cargado - {len(self.scaler.feature_names_in_)} features")

            # 2. Cargar KMeans
            kmeans_path = self.models_path / "kmeans_model.pkl"
            logger.info(f"[2/3] Cargando KMeans desde {kmeans_path}...")
            with open(kmeans_path, 'rb') as f:
                self.kmeans_model = pickle.load(f)
            
            # Verificar y forzar dtype de los centroides a float64
            if hasattr(self.kmeans_model, 'cluster_centers_'):
                logger.info(f"  Verificando dtype de centroides: {self.kmeans_model.cluster_centers_.dtype}")
                if self.kmeans_model.cluster_centers_.dtype != np.float64:
                    logger.warning(f"  ⚠️  Convirtiendo centroides de {self.kmeans_model.cluster_centers_.dtype} a float64")
                    self.kmeans_model.cluster_centers_ = self.kmeans_model.cluster_centers_.astype(np.float64)
            
            logger.info(f"  ✓ KMeans cargado - {self.kmeans_model.n_clusters} clusters")
            
            # 3. Cargar datos UMAP + KNN (NO el modelo UMAP)
            umap_path = self.models_path / "umap_data.pkl"
            logger.info(f"[3/3] Cargando datos UMAP desde {umap_path}...")
            with open(umap_path, 'rb') as f:
                umap_data = pickle.load(f)
            
            self.umap_embeddings = umap_data['embeddings']
            self.knn_index = umap_data['knn_index']
            self.feature_names = umap_data['feature_names']
            
            # Verificar y forzar dtypes correctos
            logger.info(f"  Verificando dtypes...")
            logger.info(f"    - umap_embeddings dtype: {self.umap_embeddings.dtype}")
            if hasattr(self.knn_index, '_fit_X'):
                logger.info(f"    - knn_index._fit_X dtype: {self.knn_index._fit_X.dtype}")
                # Forzar float64 en el índice KNN si es necesario
                if self.knn_index._fit_X.dtype != np.float64:
                    logger.warning(f"    ⚠️  Convirtiendo KNN index de {self.knn_index._fit_X.dtype} a float64")
                    self.knn_index._fit_X = self.knn_index._fit_X.astype(np.float64)
            
            # Asegurar que embeddings sean float64
            if self.umap_embeddings.dtype != np.float64:
                logger.warning(f"    ⚠️  Convirtiendo embeddings de {self.umap_embeddings.dtype} a float64")
                self.umap_embeddings = self.umap_embeddings.astype(np.float64)
            
            logger.info(f"  ✓ Embeddings UMAP: {self.umap_embeddings.shape}")
            logger.info(f"  ✓ KNN index: {len(self.umap_embeddings)} muestras indexadas")
            logger.info(f"  ✓ Features: {len(self.feature_names)}")
            
            logger.info("="*60)
            logger.info("MODELOS CARGADOS EXITOSAMENTE")
            logger.info("="*60)

        except FileNotFoundError as e:
            logger.error(f"❌ Archivo no encontrado: {e}")
            raise FileNotFoundError(
                f"Archivos requeridos en {self.models_path}:\n"
                "  1. scaler_model.pkl\n"
                "  2. kmeans_model.pkl\n"
                "  3. umap_data.pkl (contiene embeddings + KNN index)\n\n"
                "Ejecuta primero el script de entrenamiento (train_model.py)"
            )
        except Exception as e:
            logger.error(f"❌ Error cargando modelos: {e}", exc_info=True)
            raise
    
    def _approximate_umap(self, X_scaled: np.ndarray, n_neighbors: int = 15) -> np.ndarray:
        """
        Aproxima coordenadas UMAP usando KNN sobre datos de entrenamiento
        
        IMPORTANTE: Este método NO usa umap.transform()
        En su lugar, usa interpolación ponderada basada en vecinos cercanos
        
        Args:
            X_scaled: Datos escalados (shape: [n_samples, n_features])
            n_neighbors: Número de vecinos para aproximación
            
        Returns:
            Coordenadas UMAP aproximadas (shape: [n_samples, 2])
        """
        logger.info(f"Aproximando UMAP para {len(X_scaled)} muestras con k={n_neighbors}...")
        
        # ⭐ FIX: Asegurar que X_scaled es float64 (requiere copia para evitar warning)
        if X_scaled.dtype != np.float64:
            X_scaled = X_scaled.astype(np.float64)
        else:
            X_scaled = np.asarray(X_scaled, dtype=np.float64)
        
        logger.info(f"    Dtype de X_scaled: {X_scaled.dtype}, shape: {X_scaled.shape}")
        
        # Ajustar k si hay pocas muestras en entrenamiento
        n_neighbors = min(n_neighbors, len(self.umap_embeddings) - 1)
        
        # ⭐ FIX: Asegurar que el array es contiguo en memoria
        X_scaled = np.ascontiguousarray(X_scaled, dtype=np.float64)
        
        # Encontrar vecinos más cercanos en espacio ORIGINAL (pre-UMAP)
        distances, indices = self.knn_index.kneighbors(
            X_scaled, 
            n_neighbors=n_neighbors
        )
        
        # Inicializar array de resultados como float64
        X_umap = np.zeros((len(X_scaled), 2), dtype=np.float64)
        
        # Para cada muestra nueva
        for i in range(len(X_scaled)):
            # Calcular pesos inversamente proporcionales a distancia
            # Puntos más cercanos tienen más influencia
            weights = 1.0 / (distances[i] + 1e-10)  # +epsilon para evitar div/0
            weights = weights / weights.sum()  # Normalizar a suma 1
            
            # Obtener embeddings UMAP de los vecinos
            neighbor_embeddings = self.umap_embeddings[indices[i]]
            
            # Asegurar que neighbor_embeddings sea float64
            if neighbor_embeddings.dtype != np.float64:
                neighbor_embeddings = neighbor_embeddings.astype(np.float64)
            
            # Calcular posición UMAP como promedio ponderado
            X_umap[i] = np.sum(
                neighbor_embeddings * weights[:, np.newaxis], 
                axis=0,
                dtype=np.float64  # Forzar dtype en la suma
            )
        
        # Asegurar que el resultado final sea float64
        X_umap = X_umap.astype(np.float64)
        logger.info(f"  ✓ UMAP aproximado - Rango: [{X_umap.min():.2f}, {X_umap.max():.2f}], dtype={X_umap.dtype}")
        return X_umap
    
    def predict(self, df: pd.DataFrame) -> Tuple[np.ndarray, pd.DataFrame, pd.DataFrame]:
        """
        Realiza predicción de clusters
        
        Pasos:
        1. Validar y limpiar datos
        2. Escalar con StandardScaler
        3. Aproximar coordenadas UMAP usando KNN
        4. Predecir clusters con KMeans
        
        Args:
            df: DataFrame preprocesado completo (con todas las columnas)
            
        Returns:
            Tuple con:
            - labels: Array con cluster asignado a cada muestra
            - umap_df: DataFrame con coordenadas UMAP (UMAP_1, UMAP_2)
            - df_completo: DataFrame original con solo filas válidas
        """
        logger.info("="*60)
        logger.info(f"INICIANDO PREDICCIÓN - Input: {df.shape}")
        logger.info("="*60)
        
        # Guardar DataFrame completo
        df_completo = df.copy()
        
        # PASO 1: Seleccionar columnas numéricas
        logger.info("[Paso 1/4] Seleccionando features numéricos...")
        X = df.select_dtypes(include=["float64", "int64"])
        
        # Debug: verificar dtypes del DataFrame de entrada
        dtypes_count = df.dtypes.value_counts()
        logger.info(f"  Tipos de datos en df original: {dict(dtypes_count)}")
        logger.info(f"  ✓ {len(X.columns)} columnas numéricas detectadas")
        logger.info(f"  Tipos de datos en X: {dict(X.dtypes.value_counts())}")
        
        # PASO 2: Validar features esperados
        logger.info("[Paso 2/4] Validando features...")
        if hasattr(self.scaler, 'feature_names_in_'):
            expected_features = list(self.scaler.feature_names_in_)
            
            # Verificar columnas faltantes
            missing_features = set(expected_features) - set(X.columns)
            if missing_features:
                logger.error(f"❌ Faltan {len(missing_features)} columnas")
                raise ValueError(
                    f"Faltan columnas esperadas por el modelo:\n"
                    f"  Faltantes: {sorted(missing_features)}\n"
                    f"  Disponibles: {sorted(X.columns)}\n\n"
                    f"El modelo fue entrenado con {len(expected_features)} features."
                )
            
            # Seleccionar y ordenar columnas en el orden correcto
            X = X[expected_features]
            logger.info(f"  ✓ Features validados: {len(expected_features)} columnas en orden correcto")
            
            # Convertir TODAS las columnas a float64 explícitamente
            logger.info("  Convirtiendo todas las columnas a float64...")
            X = X.astype(np.float64)
            logger.info(f"  Tipos de datos después de conversión: {dict(X.dtypes.value_counts())}")
        
        # PASO 3: Limpiar datos (eliminar NaN)
        logger.info("[Paso 3/4] Limpiando datos...")
        indices_validos = X.dropna().index
        n_dropped = len(X) - len(indices_validos)
        
        X = X.loc[indices_validos]
        df_completo = df_completo.loc[indices_validos]
        
        if n_dropped > 0:
            logger.warning(f"  ⚠️  {n_dropped} filas eliminadas por valores nulos")
        else:
            logger.info(f"  ✓ Sin valores nulos")
        
        if X.empty:
            logger.error("❌ No hay datos válidos")
            raise ValueError(
                "No hay datos válidos después de eliminar valores faltantes.\n"
                "Verifica que tus datos tengan valores en todas las columnas requeridas."
            )
        
        logger.info(f"  ✓ Datos limpios: {len(X)} muestras × {X.shape[1]} features")
        
        # PASO 4: Pipeline de predicción
        logger.info("[Paso 4/4] Ejecutando pipeline de predicción...")
        
        # 4.1 Escalar datos
        logger.info("  [4.1] Escalando datos...")
        try:
            X_scaled = self.scaler.transform(X)
            
            # ⭐ FIX: Asegurar dtype float64 y array contiguo (evita error de buffer)
            if X_scaled.dtype != np.float64:
                logger.info(f"    Convirtiendo de {X_scaled.dtype} a float64")
                X_scaled = X_scaled.astype(np.float64)
            X_scaled = np.ascontiguousarray(X_scaled, dtype=np.float64)
            
            logger.info(f"    ✓ Escalado: media={X_scaled.mean():.3f}, std={X_scaled.std():.3f}, dtype={X_scaled.dtype}")
        except Exception as e:
            logger.error(f"    ❌ Error en escalado: {e}", exc_info=True)
            raise ValueError(f"Error al escalar datos: {e}")
        
        # 4.2 Aproximar UMAP (SIN usar umap.transform)
        logger.info("  [4.2] Aproximando embeddings UMAP con KNN...")
        try:
            X_umap = self._approximate_umap(X_scaled, n_neighbors=15)
            
            # ⭐ FIX: Asegurar dtype float64 y array contiguo
            X_umap = np.ascontiguousarray(X_umap, dtype=np.float64)
            logger.info(f"    ✓ UMAP aproximado - dtype: {X_umap.dtype}, shape: {X_umap.shape}")
        except Exception as e:
            logger.error(f"    ❌ Error en aproximación UMAP: {e}", exc_info=True)
            raise ValueError(f"Error al aproximar UMAP: {e}")        
        # 4.3 Predecir clusters
        logger.info("  [4.3] Prediciendo clusters con KMeans...")
        try:
            # Verificar dtype antes de predecir
            logger.info(f"    Dtype de X_umap antes de predict: {X_umap.dtype}")
            labels = self.kmeans_model.predict(X_umap)
        except Exception as e:
            logger.error(f"    ❌ Error en predicción KMeans: {e}", exc_info=True)
            raise ValueError(f"Error al predecir clusters: {e}")
        
        cluster_counts = np.bincount(labels)
        logger.info(f"    ✓ Distribución de clusters:")
        for cluster_id, count in enumerate(cluster_counts):
            pct = count / len(labels) * 100
            logger.info(f"      Cluster {cluster_id}: {count:4d} ({pct:5.1f}%)")
        
        # Crear DataFrame con coordenadas UMAP
        umap_df = pd.DataFrame(
            X_umap,
            columns=['UMAP_1', 'UMAP_2'],
            index=X.index
        )
        
        logger.info("="*60)
        logger.info("PREDICCIÓN COMPLETADA EXITOSAMENTE")
        logger.info("="*60)
        
        return labels, umap_df, df_completo


# Instancia global del modelo (singleton)
_clustering_model = None


def get_clustering_model() -> ClusteringModel:
    """
    Obtiene la instancia del modelo de clustering (singleton)
    
    Este patrón asegura que los modelos se cargan solo una vez
    y se reutilizan en múltiples invocaciones de Lambda
    
    Returns:
        Instancia de ClusteringModel
    """
    global _clustering_model
    if _clustering_model is None:
        logger.info("Inicializando modelo de clustering (primera vez)...")
        _clustering_model = ClusteringModel()
    else:
        logger.info("Reutilizando modelo de clustering existente")
    return _clustering_model