import matplotlib.pyplot as plt
import matplotlib.cm as cm

def plot_multi_scatterplots(df, x_column, y_columns, 
                            figsize=(15, 4), 
                            alpha=0.7,
                            marker='o',
                            s = 2,
                            title='Multiple Scatterplots'):
    """
    Create a single figure with multiple scatterplots using one x-axis column
    and multiple y-axis columns.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the data
    x_column : str
        Column name to use for x-axis
    y_columns : list
        List of column names to plot as y-axes
    figsize : tuple, optional
        Figure size (width, height) in inches
    alpha : float, optional
        Transparency of scatter points
    marker : str, optional
        Marker style for scatter points
    title : str, optional
        Title for the figure
        
    Returns:
    --------
    fig, ax : tuple
        Matplotlib figure and axis objects
    """
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Generate a color map with enough colors for all y_columns
    num_columns = len(y_columns)
    color_map = cm.get_cmap('tab10' if num_columns <= 10 else 'tab20')
    colors = [color_map(i/min(10, num_columns)) for i in range(num_columns)]
    
    # Plot each y-column against the x-column
    for i, y_col in enumerate(y_columns):
        # Get color from our generated list
        color = colors[i]
        
        # Create scatter plot
        ax.scatter(df[x_column], df[y_col], 
                   alpha=alpha,
                   marker=marker,
                   color=color,
                   label=y_col, s=s)
    
    # Add legend, title, and labels
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(x_column)
    ax.set_ylabel('Volatility')
    
    # Add grid for better readability
    ax.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    return fig, ax

def dual_axis_plot(df, x_axis, y_left_col, y_right_col, 
                  title='Dual Axis Plot', 
                  left_color='blue', right_color='red',
                  figsize=(15, 4), grid=True, 
                  left_marker=None, right_marker=None,
                  left_linestyle='-', right_linestyle='-'):
    # Make a copy of the DataFrame
    df_plot = df.copy()
    
    # Ensure datetime column is a datetime type
    # if not pd.api.types.is_datetime64_any_dtype(df_plot[datetime_col]):
    #     df_plot[datetime_col] = pd.to_datetime(df_plot[datetime_col], unit='ms')
    
    # Set default labels if not provided
    left_label = y_left_col
    right_label = y_right_col
    
    # Create figure and primary axis
    fig, ax1 = plt.subplots(figsize=figsize)
    
    # Plot data on left y-axis
    ax1.plot(df_plot[x_axis], df_plot[y_left_col], color=left_color, 
             marker=left_marker, linestyle=left_linestyle, label=left_label)
    
    # Set left y-axis properties
    ax1.set_xlabel('Date')
    ax1.set_ylabel(left_label, color=left_color)
    ax1.tick_params(axis='y', labelcolor=left_color)

    # Create secondary y-axis and plot data
    ax2 = ax1.twinx()
    ax2.plot(df_plot[x_axis], df_plot[y_right_col], color=right_color, 
             marker=right_marker, linestyle=right_linestyle, label=right_label, alpha = 0.2)
    
    # Set right y-axis properties
    ax2.set_ylabel(right_label, color=right_color)
    ax2.tick_params(axis='y', labelcolor=right_color)

    # Add grid if requested (only on the left axis to avoid visual clutter)
    if grid:
        ax1.grid(True, linestyle='--', alpha=0.5)
        ax2.grid(False)
    # Set title
    plt.title(title)
    
    # Add combined legend for both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')
    
    # Rotate date labels for better readability
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()