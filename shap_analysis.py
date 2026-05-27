"""
SHAP Analysis for Student Performance Prediction
This module demonstrates how to use SHAP to explain model predictions
"""

import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import warnings
warnings.filterwarnings('ignore')


class SHAPAnalyzer:
    """
    Analyzes student performance predictions using SHAP values
    """
    
    def __init__(self, model_path, feature_names=None):
        """
        Initialize SHAP analyzer
        
        Args:
            model_path (str): Path to trained model
            feature_names (list): List of feature names for interpretation
        """
        with open(model_path, "rb") as f:
            self.model = joblib.load(f)
        
        self.explainer = None
        self.shap_values = None
        self.feature_names = feature_names
    
    
    def load_and_prepare_data(self, csv_path, test_size=0.2, random_state=42):
        """
        Load and prepare student data
        
        Args:
            csv_path (str): Path to CSV file
            test_size (float): Proportion of data for testing
            random_state (int): Random seed
            
        Returns:
            tuple: (X_test, feature_names)
        """
        # Read data
        df = pd.read_csv(csv_path, sep=";")
        
        # Drop unnecessary columns
        if "school" in df.columns:
            df = df.drop(columns="school")
        
        # Encode categorical variables
        le = OneHotEncoder()
        categorical_cols = df.select_dtypes(include="object").columns
        
        for col in categorical_cols:
            df[col] = le.fit_transform(df[col])
        
        # Separate features and labels (drop grade columns)
        X = df.drop(columns=["G1", "G2", "G3"], errors='ignore')
        
        # Store feature names if not provided
        if self.feature_names is None:
            self.feature_names = X.columns.tolist()
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Split data
        from sklearn.model_selection import train_test_split
        X_train, X_test, _, _ = train_test_split(
            X_scaled, X.values, test_size=test_size, random_state=random_state
        )
        
        return X_test, X_train, self.feature_names
    
    
    def create_explainer(self, background_data, model_type="tree"):
        """
        Create SHAP explainer
        
        Args:
            background_data: Sample of training data for reference
            model_type (str): Type of explainer - "tree", "kernel", or "linear"
        """
        # Extract the actual model if it's a Pipeline
        model_to_explain = self._extract_estimator()
        
        if model_type == "tree":
            self.explainer = shap.TreeExplainer(model_to_explain)
        elif model_type == "kernel":
            self.explainer = shap.KernelExplainer(model_to_explain.predict, background_data)
        else:
            self.explainer = shap.LinearExplainer(model_to_explain, background_data)
        
        print(f"✓ {model_type.upper()} SHAP Explainer created successfully")
    
    
    def _extract_estimator(self):
        """
        Extract the underlying estimator from a Pipeline if needed.
        TreeExplainer doesn't support Pipeline objects (sklearn or imblearn),
        so we need the actual tree-based model.
        
        Supports:
        - sklearn.pipeline.Pipeline
        - imblearn.pipeline.Pipeline
        
        Returns:
            The model or the final estimator from a Pipeline
        """
        try:
            # Try sklearn Pipeline first
            from sklearn.pipeline import Pipeline as SklearnPipeline
            if isinstance(self.model, SklearnPipeline):
                estimator = self.model.named_steps[self.model.steps[-1][0]]
                print(f"✓ Extracted estimator from sklearn Pipeline: {type(estimator).__name__}")
                return estimator
        except ImportError:
            pass
        
        try:
            # Try imblearn Pipeline
            from imblearn.pipeline import Pipeline as ImbPipeline
            if isinstance(self.model, ImbPipeline):
                estimator = self.model.named_steps[self.model.steps[-1][0]]
                print(f"✓ Extracted estimator from imblearn Pipeline: {type(estimator).__name__}")
                return estimator
        except ImportError:
            pass
        
        # If not a pipeline, return the model as-is
        return self.model
    
    
    def compute_shap_values(self, X_test):
        """
        Compute SHAP values for test data
        
        Args:
            X_test: Test feature data (will be transformed through pipeline if needed)
        """
        if self.explainer is None:
            raise ValueError("Explainer not initialized. Call create_explainer first.")
        
        # If model is a Pipeline, we need to preprocess the data
        X_to_explain = self._transform_data(X_test)
        
        self.shap_values = self.explainer.shap_values(X_to_explain)
        print(f"✓ SHAP values computed for {len(X_to_explain)} samples")
    
    
    def _transform_data(self, X):
        """
        Transform data through pipeline preprocessing steps if needed.
        
        Handles both sklearn and imblearn pipelines by extracting
        all preprocessing steps and applying them before SHAP analysis.
        
        Args:
            X: Raw feature data
            
        Returns:
            Preprocessed data
        """
        is_pipeline = False
        pipeline_type = None
        
        try:
            from sklearn.pipeline import Pipeline as SklearnPipeline
            if isinstance(self.model, SklearnPipeline):
                is_pipeline = True
                pipeline_type = "sklearn"
        except ImportError:
            pass
        
        if not is_pipeline:
            try:
                from imblearn.pipeline import Pipeline as ImbPipeline
                if isinstance(self.model, ImbPipeline):
                    is_pipeline = True
                    pipeline_type = "imblearn"
            except ImportError:
                pass
        
        if is_pipeline:
            # Get all steps except the final estimator
            n_steps = len(self.model.steps)
            if n_steps > 1:
                # Create a pipeline with all preprocessing steps
                preprocessing_steps = self.model.steps[:-1]
                
                if pipeline_type == "imblearn":
                    from imblearn.pipeline import Pipeline
                else:
                    from sklearn.pipeline import Pipeline
                
                preprocessor = Pipeline(preprocessing_steps)
                X_transformed = preprocessor.transform(X)
                print(f"✓ Data transformed through {len(preprocessing_steps)} {pipeline_type} preprocessing step(s)")
                return X_transformed
        
        return X
    
    
    def global_feature_importance(self, figsize=(12, 6), show_plot=True):
        """
        Show global feature importance using mean absolute SHAP values
        
        Args:
            figsize (tuple): Figure size
            show_plot (bool): Whether to display plot
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not computed. Call compute_shap_values first.")
        
        # Handle multiple outputs (if model returns array)
        if isinstance(self.shap_values, list):
            shap_vals = self.shap_values[0]
        else:
            shap_vals = self.shap_values
        
        plt.figure(figsize=figsize)
        shap.summary_plot(shap_vals, feature_names=self.feature_names, 
                         plot_type="bar", show=False)
        plt.title("Global Feature Importance (Mean |SHAP values|)", fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        
        return plt.gcf()
    
    
    def shap_summary_plot(self, figsize=(12, 8), show_plot=True):
        """
        Create SHAP summary plot (Beeswarm plot)
        
        Args:
            figsize (tuple): Figure size
            show_plot (bool): Whether to display plot
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not computed. Call compute_shap_values first.")
        
        # Handle multiple outputs
        if isinstance(self.shap_values, list):
            shap_vals = self.shap_values[0]
        else:
            shap_vals = self.shap_values
        
        plt.figure(figsize=figsize)
        shap.summary_plot(shap_vals, feature_names=self.feature_names, show=False)
        plt.title("SHAP Summary Plot - Feature Impact on Predictions", 
                 fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        
        return plt.gcf()
    
    
    def local_explanation(self, sample_index, X_test, figsize=(12, 6), show_plot=True):
        """
        Explain a single prediction
        
        Args:
            sample_index (int): Index of sample to explain
            X_test: Test data
            figsize (tuple): Figure size
            show_plot (bool): Whether to display plot
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not computed. Call compute_shap_values first.")
        
        # Handle multiple outputs
        if isinstance(self.shap_values, list):
            shap_vals = self.shap_values[0]
        else:
            shap_vals = self.shap_values
        
        plt.figure(figsize=figsize)
        shap.force_plot(self.explainer.expected_value, shap_vals[sample_index], 
                       X_test[sample_index], feature_names=self.feature_names, matplotlib=True)
        plt.title(f"SHAP Force Plot - Student Sample #{sample_index}", 
                 fontsize=12, fontweight='bold')
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        
        return plt.gcf()
    
    
    def feature_dependence_plot(self, feature_name, figsize=(10, 6), show_plot=True):
        """
        Show how a specific feature affects predictions
        
        Args:
            feature_name (str): Name of feature to analyze
            figsize (tuple): Figure size
            show_plot (bool): Whether to display plot
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not computed. Call compute_shap_values first.")
        
        if feature_name not in self.feature_names:
            raise ValueError(f"Feature '{feature_name}' not found in feature list")
        
        feature_idx = self.feature_names.index(feature_name)
        
        # Handle multiple outputs
        if isinstance(self.shap_values, list):
            shap_vals = self.shap_values[0]
        else:
            shap_vals = self.shap_values
        
        plt.figure(figsize=figsize)
        shap.dependence_plot(feature_idx, shap_vals, feature_names=self.feature_names, 
                            show=False)
        plt.title(f"Dependence Plot: {feature_name}", fontsize=12, fontweight='bold')
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        
        return plt.gcf()
    
    
    def get_top_features_for_prediction(self, sample_index, top_n=5):
        """
        Get top N features influencing a specific prediction
        
        Args:
            sample_index (int): Index of sample
            top_n (int): Number of top features to return
            
        Returns:
            DataFrame: Top features with their SHAP values
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not computed. Call compute_shap_values first.")
        
        # Handle multiple outputs
        if isinstance(self.shap_values, list):
            shap_vals = self.shap_values[0]
        else:
            shap_vals = self.shap_values
        
        # Get absolute SHAP values for the sample
        sample_shap = np.abs(shap_vals[sample_index])
        
        # Create dataframe with feature names and SHAP values
        importance_df = pd.DataFrame({
            'Feature': self.feature_names,
            'SHAP_Value': shap_vals[sample_index],
            'Abs_SHAP_Value': sample_shap
        }).sort_values('Abs_SHAP_Value', ascending=False)
        
        return importance_df.head(top_n)


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    
    # Initialize analyzer
    print("=" * 60)
    print("SHAP Analysis for Student Performance Prediction")
    print("=" * 60)
    
    analyzer = SHAPAnalyzer("ml_model/stud_performance_classifier.joblib")
    
    # Load data
    print("\n1. Loading and preparing data...")
    X_test, X_train, feature_names = analyzer.load_and_prepare_data("data/student-mat.csv")
    print(f"   ✓ Data loaded: {len(X_test)} test samples, {len(feature_names)} features")
    
    # Create explainer
    print("\n2. Creating SHAP Explainer...")
    analyzer.create_explainer(X_train, model_type="tree")
    
    # Compute SHAP values
    print("\n3. Computing SHAP values...")
    analyzer.compute_shap_values(X_test)
    
    # Global Analysis
    print("\n4. Global Feature Importance Analysis")
    print("   Generating importance plot...")
    analyzer.global_feature_importance()
    
    # Summary plot
    print("\n5. SHAP Summary Plot")
    print("   Generating summary plot...")
    analyzer.shap_summary_plot()
    
    # Local explanation for a specific student
    print("\n6. Local Explanation for Student #0")
    top_features = analyzer.get_top_features_for_prediction(0, top_n=5)
    print("\n   Top 5 Features Affecting This Student's Prediction:")
    print(top_features.to_string())
    analyzer.local_explanation(0, X_test)
    
    # Feature dependence
    if len(feature_names) > 0:
        print(f"\n7. Feature Dependence Analysis ({feature_names[0]})")
        analyzer.feature_dependence_plot(feature_names[0])
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
