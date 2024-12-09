from ..core.base import BaseModel
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import umap
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.feature_selection import SelectKBest, mutual_info_classif
import shap
import optuna
from scipy.stats import chi2_contingency, f_oneway
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

class AdvancedSegmentationModel(BaseModel):
    """
    Gelişmiş Müşteri Segmentasyon Modeli
    
    Özellikler:
    - Çoklu segmentasyon yöntemleri
    - Otomatik özellik seçimi
    - Segment profilleme
    - Segment geçiş analizi
    - Segment performans analizi
    """
    
    def __init__(self,
                 method: str = 'kmeans',
                 n_segments: int = 5,
                 feature_selection: bool = True,
                 n_features: Optional[int] = None,
                 random_state: int = 42):
        super().__init__()
        self.method = method
        self.n_segments = n_segments
        self.feature_selection = feature_selection
        self.n_features = n_features
        self.random_state = random_state
        
        # Model bileşenleri
        self.clustering_model = None
        self.feature_selector = None
        self.scaler = StandardScaler()
        self.dim_reducer = PCA(n_components=2, random_state=self.random_state)
        self.selected_features = None
        self.segment_profiles = None
        self.segment_transitions = None
        
        self._initialize_models()
        
    def _initialize_models(self):
        """Model bileşenlerini başlat"""
        # Kümeleme modeli seçimi
        if self.method == 'kmeans':
            self.clustering_model = KMeans(
                n_clusters=self.n_segments,
                random_state=self.random_state
            )
        elif self.method == 'gmm':
            self.clustering_model = GaussianMixture(
                n_components=self.n_segments,
                random_state=self.random_state
            )
        elif self.method == 'dbscan':
            self.clustering_model = DBSCAN(
                eps=0.5,
                min_samples=5
            )
        elif self.method == 'hierarchical':
            self.clustering_model = AgglomerativeClustering(
                n_clusters=self.n_segments
            )
            
        # Boyut indirgeme
        self.dim_reducer = PCA(
            n_components=2,
            random_state=self.random_state
        )
        
    def _optimize_hyperparameters(self,
                                X: np.ndarray,
                                n_trials: int = 50) -> Dict:
        """Hyperparameter optimizasyonu"""
        def objective(trial):
            if self.method == 'kmeans':
                model = KMeans(
                    n_clusters=trial.suggest_int('n_clusters', 2, 10),
                    random_state=self.random_state
                )
            elif self.method == 'dbscan':
                model = DBSCAN(
                    eps=trial.suggest_loguniform('eps', 0.01, 1.0),
                    min_samples=trial.suggest_int('min_samples', 2, 10)
                )
            
            clusters = model.fit_predict(X)
            if len(np.unique(clusters)) < 2:
                return float('-inf')
                
            return silhouette_score(X, clusters)
            
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials)
        
        return study.best_params
        
    def _select_features(self,
                        X: pd.DataFrame,
                        y: Optional[np.ndarray] = None) -> pd.DataFrame:
        """Özellik seçimi"""
        if not self.feature_selection:
            return X
            
        if y is not None:
            # Supervised feature selection
            self.feature_selector = SelectKBest(
                score_func=mutual_info_classif,
                k=self.n_features or int(X.shape[1] * 0.5)
            )
            self.feature_selector.fit(X, y)
            selected_features = X.columns[self.feature_selector.get_support()]
        else:
            # Unsupervised feature selection (variance based)
            selector = VarianceThreshold(threshold=0.01)
            selector.fit(X)
            selected_features = X.columns[selector.get_support()]
            
        self.selected_features = selected_features
        return X[selected_features]
        
    def _calculate_segment_profiles(self,
                                  X: pd.DataFrame,
                                  segments: np.ndarray) -> Dict:
        """Segment profillerini hesapla"""
        profiles = {}
        
        for segment_id in np.unique(segments):
            segment_mask = segments == segment_id
            segment_data = X[segment_mask]
            
            profiles[f"Segment_{segment_id}"] = {
                'size': len(segment_data),
                'percentage': len(segment_data) / len(X) * 100,
                'mean': segment_data.mean(),
                'std': segment_data.std(),
                'median': segment_data.median(),
                'characteristics': self._get_segment_characteristics(segment_data, X)
            }
            
        return profiles
        
    def _get_segment_characteristics(self,
                                   segment_data: pd.DataFrame,
                                   full_data: pd.DataFrame) -> Dict:
        """Segment karakteristiklerini belirle"""
        characteristics = {}
        
        for column in segment_data.columns:
            if pd.api.types.is_numeric_dtype(segment_data[column]):
                # Sayısal değişkenler için t-test
                t_stat, p_value = stats.ttest_ind(
                    segment_data[column],
                    full_data[column]
                )
                if p_value < 0.05:
                    characteristics[column] = {
                        'difference': segment_data[column].mean() - full_data[column].mean(),
                        'significance': p_value
                    }
            else:
                # Kategorik değişkenler için chi-square test
                contingency = pd.crosstab(
                    pd.Series(segment_data[column]),
                    pd.Series(full_data[column])
                )
                chi2, p_value, _, _ = chi2_contingency(contingency)
                if p_value < 0.05:
                    characteristics[column] = {
                        'most_common': segment_data[column].mode()[0],
                        'significance': p_value
                    }
                    
        return characteristics
        
    def fit(self,
            X: pd.DataFrame,
            y: Optional[np.ndarray] = None) -> 'AdvancedSegmentationModel':
        """
        Model eğitimi
        
        Parameters:
        -----------
        X: Özellik matrisi
        y: Hedef değişken (opsiyonel, özellik seçimi için)
        """
        # Özellik seçimi
        if self.feature_selection:
            X = self._select_features(X, y)
            
        # Veri ölçeklendirme
        X_scaled = self.scaler.fit_transform(X)
        
        # Hyperparameter optimizasyonu
        if self.method in ['kmeans', 'dbscan']:
            best_params = self._optimize_hyperparameters(X_scaled)
            self.clustering_model.set_params(**best_params)
            
        # Model eğitimi
        self.clustering_model.fit(X_scaled)
        
        # Segment profilleri
        segments = self.clustering_model.predict(X_scaled)
        self.segment_profiles = self._calculate_segment_profiles(X, segments)
        
        self.is_fitted = True
        return self
        
    def predict(self,
               X: pd.DataFrame) -> np.ndarray:
        """Segment tahminleri"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
            
        # Özellik seçimi
        if self.feature_selection and self.selected_features is not None:
            X = X[self.selected_features]
            
        X_scaled = self.scaler.transform(X)
        return self.clustering_model.predict(X_scaled)
        
    def analyze_segments(self,
                        X: pd.DataFrame,
                        segments: np.ndarray,
                        target_variable: Optional[pd.Series] = None) -> Dict:
        """
        Segment analizi
        
        Parameters:
        -----------
        X: Özellik matrisi
        segments: Segment etiketleri
        target_variable: Hedef değişken (opsiyonel)
        """
        analysis = {}
        
        # Temel segment metrikleri
        analysis['segment_metrics'] = {
            'silhouette_score': silhouette_score(X, segments),
            'calinski_harabasz_score': calinski_harabasz_score(X, segments)
        }
        
        # Segment büyüklükleri ve dağılımı
        segment_sizes = pd.Series(segments).value_counts()
        analysis['segment_distribution'] = {
            'sizes': segment_sizes.to_dict(),
            'entropy': -np.sum(
                (segment_sizes / len(segments)) * np.log(segment_sizes / len(segments))
            )
        }
        
        # Özellik önem skorları
        if self.method in ['kmeans', 'gmm']:
            feature_importance = pd.DataFrame(
                self.clustering_model.cluster_centers_,
                columns=X.columns
            ).std()
            analysis['feature_importance'] = feature_importance.to_dict()
            
        # Hedef değişken analizi
        if target_variable is not None:
            analysis['target_analysis'] = self._analyze_target_by_segment(
                segments,
                target_variable
            )
            
        # Segment geçiş olasılıkları (eğer zaman serisi varsa)
        if hasattr(X, 'index') and isinstance(X.index, pd.DatetimeIndex):
            analysis['transition_matrix'] = self._calculate_transition_matrix(segments)
            
        return analysis
        
    def _analyze_target_by_segment(self,
                                 segments: np.ndarray,
                                 target: pd.Series) -> Dict:
        """Hedef değişken analizi"""
        analysis = {}
        
        if pd.api.types.is_numeric_dtype(target):
            # ANOVA analizi
            f_stat, p_value = f_oneway(*[
                target[segments == segment]
                for segment in np.unique(segments)
            ])
            
            # Tukey HSD post-hoc analizi
            tukey = pairwise_tukeyhsd(target, segments)
            
            analysis['anova'] = {
                'f_statistic': f_stat,
                'p_value': p_value,
                'tukey_results': str(tukey)
            }
        else:
            # Chi-square analizi
            contingency = pd.crosstab(segments, target)
            chi2, p_value, dof, expected = chi2_contingency(contingency)
            
            analysis['chi_square'] = {
                'statistic': chi2,
                'p_value': p_value,
                'dof': dof
            }
            
        return analysis
        
    def _calculate_transition_matrix(self,
                                   segments: np.ndarray) -> pd.DataFrame:
        """Segment geçiş matrisini hesapla"""
        transitions = pd.DataFrame(
            np.zeros((self.n_segments, self.n_segments)),
            index=[f"Segment_{i}" for i in range(self.n_segments)],
            columns=[f"Segment_{i}" for i in range(self.n_segments)]
        )
        
        for i in range(len(segments)-1):
            transitions.loc[
                f"Segment_{segments[i]}",
                f"Segment_{segments[i+1]}"
            ] += 1
            
        # Normalize
        transitions = transitions.div(transitions.sum(axis=1), axis=0)
        
        return transitions
        
    def get_segment_recommendations(self,
                                  segment_id: int,
                                  X: pd.DataFrame) -> Dict:
        """Segment bazlı öneriler"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
            
        segment_mask = self.predict(X) == segment_id
        segment_data = X[segment_mask]
        
        recommendations = {
            'targeting': self._get_targeting_recommendations(segment_data),
            'marketing_mix': self._get_marketing_mix_recommendations(segment_data),
            'growth_potential': self._calculate_growth_potential(segment_data, X)
        }
        
        return recommendations
        
    def _get_targeting_recommendations(self,
                                     segment_data: pd.DataFrame) -> Dict:
        """Hedefleme önerileri"""
        profile = segment_data.mean()
        
        return {
            'ideal_customer_profile': profile.to_dict(),
            'targeting_channels': self._recommend_channels(profile),
            'messaging_themes': self._recommend_messaging(profile)
        }
        
    def _get_marketing_mix_recommendations(self,
                                         segment_data: pd.DataFrame) -> Dict:
        """Pazarlama karması önerileri"""
        return {
            'price_sensitivity': self._calculate_price_sensitivity(segment_data),
            'promotion_effectiveness': self._analyze_promotion_effectiveness(segment_data),
            'channel_preferences': self._analyze_channel_preferences(segment_data)
        }
        
    def _calculate_growth_potential(self,
                                  segment_data: pd.DataFrame,
                                  full_data: pd.DataFrame) -> Dict:
        """Büyüme potansiyeli analizi"""
        return {
            'market_share': len(segment_data) / len(full_data),
            'value_potential': self._calculate_value_potential(segment_data),
            'expansion_opportunities': self._identify_expansion_opportunities(segment_data)
        }