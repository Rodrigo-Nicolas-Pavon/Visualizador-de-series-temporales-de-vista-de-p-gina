import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar y limpiar los datos
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Limpiar los datos (filtrar el 2.5% superior e inferior)
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

# Función para dibujar el gráfico de líneas
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    
    # Título y etiquetas
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    # Guardar figura
    fig.savefig('line_plot.png')
    return fig

# Función para dibujar el gráfico de barras
def draw_bar_plot():
    # Copiar y preparar datos para el gráfico de barras
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Agrupar datos por año y mes, calcular el promedio
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Dibujar el gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(10, 8), legend=True).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    plt.xticks(rotation=45)

    # Guardar figura
    fig.savefig('bar_plot.png')
    return fig

# Función para dibujar los diagramas de caja
def draw_box_plot():
    # Copiar y preparar los datos para los diagramas de caja
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Ordenar los meses de enero a diciembre
    df_box['month'] = pd.Categorical(df_box['month'], categories=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ], ordered=True)

    # Dibujar el gráfico de cajas lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Guardar figura
    fig.savefig('box_plot.png')
    return fig

# Ejecutar el código para probar los gráficos
if __name__ == "__main__":
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()
