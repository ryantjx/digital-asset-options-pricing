import numpy as np
import pandas as pd

def simple_historical_volatility(df, window=20, scaling=np.sqrt(252), log_return_col='log_return'):
    """
    Calculate Simple Historical Volatility (Close-to-Close)
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with OHLCV data and log returns
    window : int, default 20
        Rolling window for volatility calculation (e.g., 20 days)
    scaling : float, default sqrt(252)
        Annualization factor (√252 for daily, √12 for monthly, √4 for quarterly)
    log_return_col : str, default 'log_return'
        Name of the column containing log returns
        
    Returns:
    --------
    pandas.Series
        Series with calculated simple historical volatility
    """
    # Standard deviation of log returns
    return df[log_return_col].rolling(window=window).std() * scaling


def parkinson_volatility(df, window=20, scaling=np.sqrt(252), high_col='high', low_col='low'):
    """
    Calculate Parkinson Volatility using high-low range
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with OHLCV data
    window : int, default 20
        Rolling window for volatility calculation (e.g., 20 days)
    scaling : float, default sqrt(252)
        Annualization factor
    high_col : str, default 'high'
        Name of the high price column
    low_col : str, default 'low'
        Name of the low price column
        
    Returns:
    --------
    pandas.Series
        Series with calculated Parkinson volatility
    """
    # Formula: σ_p = sqrt(1/(4*ln(2)) * sum[(ln(high/low))^2] / n)
    high_low_ratio = df[high_col] / df[low_col]
    log_high_low = np.log(high_low_ratio)
    
    return np.sqrt(
        1.0 / (4.0 * np.log(2.0)) * 
        log_high_low.pow(2).rolling(window=window).mean()
    ) * scaling


def garman_klass_volatility(df, window=20, scaling=np.sqrt(252), 
                            high_col='high', low_col='low', 
                            open_col='open', close_col='close'):
    """
    Calculate Garman-Klass Volatility
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with OHLCV data
    window : int, default 20
        Rolling window for volatility calculation (e.g., 20 days)
    scaling : float, default sqrt(252)
        Annualization factor
    high_col, low_col, open_col, close_col : str
        Names of the respective price columns
        
    Returns:
    --------
    pandas.Series
        Series with calculated Garman-Klass volatility
    """
    # Formula: σ_gk = sqrt(0.5 * [ln(high/low)]^2 - (2*ln(2)-1) * [ln(close/open)]^2)
    high_low = np.log(df[high_col] / df[low_col]).pow(2)
    close_open = np.log(df[close_col] / df[open_col]).pow(2)
    
    return np.sqrt(
        (0.5 * high_low - (2 * np.log(2) - 1) * close_open).rolling(window=window).mean()
    ) * scaling


def rogers_satchell_volatility(df, window=20, scaling=np.sqrt(252),
                               high_col='high', low_col='low', 
                               open_col='open', close_col='close'):
    """
    Calculate Rogers-Satchell Volatility
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with OHLCV data
    window : int, default 20
        Rolling window for volatility calculation (e.g., 20 days)
    scaling : float, default sqrt(252)
        Annualization factor
    high_col, low_col, open_col, close_col : str
        Names of the respective price columns
        
    Returns:
    --------
    pandas.Series
        Series with calculated Rogers-Satchell volatility
    """
    # Formula: σ_rs = sqrt(ln(high/close) * ln(high/open) + ln(low/close) * ln(low/open))
    high_close = np.log(df[high_col] / df[close_col])
    high_open = np.log(df[high_col] / df[open_col])
    low_close = np.log(df[low_col] / df[close_col])
    low_open = np.log(df[low_col] / df[open_col])
    
    return np.sqrt(
        (high_close * high_open + low_close * low_open).rolling(window=window).mean()
    ) * scaling


def yang_zhang_volatility(df, window=20, scaling=np.sqrt(252), k=0.34,
                          high_col='high', low_col='low', 
                          open_col='open', close_col='close'):
    """
    Calculate Yang-Zhang Volatility (combines overnight and intraday volatility)
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with OHLCV data
    window : int, default 20
        Rolling window for volatility calculation (e.g., 20 days)
    scaling : float, default sqrt(252)
        Annualization factor
    k : float, default 0.34
        Weighting parameter for efficiency
    high_col, low_col, open_col, close_col : str
        Names of the respective price columns
        
    Returns:
    --------
    pandas.Series
        Series with calculated Yang-Zhang volatility
    """
    # Calculate overnight returns (close to next open)
    df_copy = df.copy()
    df_copy['overnight_return'] = np.log(df_copy[open_col] / df_copy[close_col].shift(1))
    
    # Calculate open-to-close returns
    df_copy['open_close_return'] = np.log(df_copy[close_col] / df_copy[open_col])
    
    # Calculate overnight volatility component
    overnight_vol = df_copy['overnight_return'].rolling(window=window).var()
    
    # Calculate open-to-close volatility component
    open_close_vol = df_copy['open_close_return'].rolling(window=window).var()
    
    # Calculate Rogers-Satchell volatility for the intraday part
    rs_vol = rogers_satchell_volatility(df, window=window, scaling=1.0,
                                        high_col=high_col, low_col=low_col, 
                                        open_col=open_col, close_col=close_col)
    
    # Combine components: σ²_yz = σ²_overnight + k*σ²_open-close + (1-k)*σ²_RS
    yang_zhang = overnight_vol + k * open_close_vol + (1-k) * rs_vol**2
    
    # Take square root and scale
    return np.sqrt(yang_zhang) * scaling


def calculate_all_volatilities(df, window=20, scaling=np.sqrt(252),
                               high_col='high', low_col='low', 
                               open_col='open', close_col='close',
                               log_return_col='log_return'):
    """
    Calculate all volatility measures and return them in a DataFrame
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with OHLCV data and log returns
    window : int, default 20
        Rolling window for volatility calculation
    scaling, high_col, low_col, open_col, close_col, log_return_col:
        See individual function documentation
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with all calculated volatility measures
    """
    result = pd.DataFrame(index=df.index)
    
    # Calculate each volatility measure
    result['simple_vol'] = simple_historical_volatility(
        df, window=window, scaling=scaling, log_return_col=log_return_col)
    
    result['parkinson_vol'] = parkinson_volatility(
        df, window=window, scaling=scaling, high_col=high_col, low_col=low_col)
    
    result['garman_klass_vol'] = garman_klass_volatility(
        df, window=window, scaling=scaling, 
        high_col=high_col, low_col=low_col, open_col=open_col, close_col=close_col)
    
    result['rogers_satchell_vol'] = rogers_satchell_volatility(
        df, window=window, scaling=scaling,
        high_col=high_col, low_col=low_col, open_col=open_col, close_col=close_col)
    
    result['yang_zhang_vol'] = yang_zhang_volatility(
        df, window=window, scaling=scaling,
        high_col=high_col, low_col=low_col, open_col=open_col, close_col=close_col)
    
    return result