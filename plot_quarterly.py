import matplotlib.pyplot as plt
from datetime import datetime


def plot_quarterly(model_name, mean_predictions, ci_95_half_widths, y_test_2014):
    def add_date_index(values):
        return pd.Series(values, 
                         index=pd.date_range(start=datetime(2014, 1, 1), end=datetime(2014, 12, 30)))
                
    def rmse(prediction_errors):
        return (prediction_errors ** 2).mean() ** 0.5
    
    plt.tight_layout()
    for i, (quarter, from_date_inclusive, to_date_non_inclusive) in enumerate([
        ('Q1', datetime(2014, 1, 1), datetime(2014, 4, 1)),
        ('Q2', datetime(2014, 4, 1), datetime(2014, 7, 1)),
        ('Q3', datetime(2014, 7, 1), datetime(2014, 10, 1)),
        ('Q4', datetime(2014, 10, 1), datetime(2014, 12, 31))
    ]):    
        def filter_date_range(series):
            return series\
                [lambda df: df.index >= from_date_inclusive]\
                [lambda df: df.index < to_date_non_inclusive]

        plt.subplot(411 + i)
        plt.plot(filter_date_range(y_test_2014), "b-", label='Actual', lw=1.5)
        plt.plot(filter_date_range(mean_predictions), "r-x", label='Predicted', lw=1)
        plt.fill_between(filter_date_range(y_test_2014).index, 
                         filter_date_range(mean_predictions + ci_95_half_widths),
                         filter_date_range(mean_predictions - ci_95_half_widths),
                         color='lightgrey', label='95% C.I.')
        plt.legend(loc='lower left', fontsize=12)
        plt.text(0.01, 0.9, quarter, fontsize=20,
                 horizontalalignment='left', verticalalignment='center', transform=plt.gca().transAxes)
        if i == 0:
            plt.title(model_name, fontsize=20)
    
    return rmse(mean_predictions - y_test_2014)