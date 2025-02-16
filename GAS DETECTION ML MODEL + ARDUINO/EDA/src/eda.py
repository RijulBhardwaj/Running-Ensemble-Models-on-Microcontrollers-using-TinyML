import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
from sklearn.feature_selection import mutual_info_classif

def distribution_analysis(data, predictors, output_dir):
    """Generate KDE plots for feature distribution."""
    os.makedirs(output_dir, exist_ok=True)
    for column in predictors:
        fig, ax1 = plt.subplots()

        sns.histplot(data[column], ax=ax1, color='skyblue', alpha=0.5)
        ax1.set_xlabel(column)
        ax1.set_ylabel('Count')

        ax2 = ax1.twinx()
        sns.kdeplot(data[column], ax=ax2, color='red')
        ax2.set_ylabel('Density')

        plt.title(column)
        plt.savefig(f"{output_dir}/{column}_distribution.png")
        plt.close()

def outlier_check(data, predictors, output_dir):
    """Generate box plots for outlier detection."""
    os.makedirs(output_dir, exist_ok=True)
    fig = plt.figure(figsize=(10, 20))
    fig.suptitle("Tukey's Outlier Detection for Each Predictor Feature")

    for i, column in enumerate(predictors):
        ax = plt.subplot(4, 2, i + 1)
        sns.boxplot(data[column], whis=1.5, ax=ax)
        ax.set_title(f"Outlier Visualization (IQR) for {column}")

    plt.tight_layout()
    plt.savefig(f"{output_dir}/outliers.png")
    plt.close()

def statistical_data_analysis(data):
    """Display data info, null counts, and descriptive statistics."""
    print(data.info())
    print(data.isnull().sum())
    print(data.describe())

def class_distribution_check(data, target_column, output_dir):
    """Check target class distribution."""
    os.makedirs(output_dir, exist_ok=True)
    sns.countplot(data=data, x=target_column)
    plt.title("Class Distribution")
    plt.savefig(f"{output_dir}/class_distribution_countplot.png")
    plt.close()

    plt.figure(figsize=(5, 5))
    data[target_column].value_counts().plot(kind='pie', autopct='%.2f%%')
    plt.title("Class Distribution (Pie)")
    plt.axis('equal')
    plt.savefig(f"{output_dir}/class_distribution_pie.png")
    plt.close()

def correlation_analysis(data, output_dir):
    """Generate correlation heatmap."""
    os.makedirs(output_dir, exist_ok=True)
    corr_matrix = data.corr(numeric_only=True)
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
    plt.title("Feature Correlation Matrix")
    plt.savefig(f"{output_dir}/correlation_matrix.png")
    plt.close()

def feature_importance_analysis(data, predictors, target_column, output_dir):
    """Compute and plot feature importance using mutual information."""
    os.makedirs(output_dir, exist_ok=True)
    X = data[predictors]
    y = data[target_column]
    mutual_info_scores = mutual_info_classif(X, y)

    feature_importance = pd.DataFrame({
        'Features': predictors,
        'Mutual Info': mutual_info_scores
    }).sort_values(by='Mutual Info', ascending=False)

    plt.bar(feature_importance['Features'], feature_importance['Mutual Info'])
    plt.xlabel('Features')
    plt.ylabel('Mutual Info')
    plt.title('Mutual Info for Each Feature')
    plt.savefig(f"{output_dir}/feature_importance.png")
    plt.close()
