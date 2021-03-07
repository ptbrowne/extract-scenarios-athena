import re
import pandas as pd

def parse_stats_from_file(filename, limit=10):
    """Extraire d'un CSV les scenarios"""
    with open(filename, 'rb') as csvfile:
        for line in csvfile:
            if line.startswith('#   fit'):
                # Need to do a bit of a hack since the first column is named
                # "fit #" and the space make the splitter thinks its two
                # different columns
                column_names = re.split(r'\s+', line.strip())[1:]
                column_names = ['fit'] + column_names[2:]

    with open(filename, 'rb') as csvfile:
        df = pd.read_csv(
            csvfile,
            comment='#',
            sep="\\s+",
            names=column_names
        )

    return df


def format_pair(pair):
    return '%.2f x %s' % (pair[0], pair[1].replace('.xmu', '').replace('.nor', ''))


def count_refs_from_stats(stats):
    all_refs = stats.columns[7:-1]
    return len(all_refs)


def summary_from_data(stats, fits):
    all_refs = stats.columns[7:-1]

    refs_table = [
        sorted([
            (row[ref], ref) for ref in all_refs if row[ref] > 0
        ])[::-1] 
        for index, row in stats.iterrows()
    ]

    df = pd.DataFrame(stats[['fit', 'chi2', 'chi2_reduced']])

    nb_refs = len(refs_table[0])
    for n in range(len(refs_table[0])): 
        df['ref #%s' % (n + 1)] = [format_pair(pairs[n]) for pairs in refs_table]


    r_stats = compute_r_from_fits(fits)
    df['r2'] = [
        r_stats['r2_fit_0%i' % i] for i in range(stats.shape[0])
    ]

    return df

# ---------

def parse_fits_from_file(filename, limit=10):
    """Extraire d'un CSV les scenarios"""
    with open(filename, 'rb') as csvfile:
        for line in csvfile:
            if line.startswith('#   energy'):
                column_names = re.split(r'\s+', line.strip())[1:]
    with open(filename, 'rb') as csvfile:
        df = pd.read_csv(
            csvfile,
            comment='#',
            sep="\\s+",
            index_col=False,
            names=column_names
        )

    fit_columns = [col for col in df.columns if col.startswith('fit_')]

    for col in fit_columns:
        df['error_%s' % col] = ((df[col] - df['data']) ** 2)

    return df


def compute_r_from_fits(df):
    fit_columns = [col for col in df.columns if col.startswith('fit_')]
    sum_data_squared = (df['data'] ** 2).sum()
    res = {}
    for col in fit_columns:
        res['r2_%s' % col] = df['error_%s' % col].sum() / sum_data_squared
    return res
