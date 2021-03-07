# -*- coding: utf-8 -*-
import os.path as osp
import argparse
import sys
import pandas as pd

from glob import glob
from jinja2 import Template
from termcolor import colored
from IPython.display import display, Image, HTML

from parse import parse_stats_from_file, parse_fits_from_file, summary_from_data, compute_r_from_fits, count_refs_from_stats
from notebook import Notebook
from subprocess import call

def render(template, **data):
    return Template(template).render(data)

def has_images(path, scenario):
    scenario_id = scenario.id
    n_refs = len(scenario.refs)
    pattern = '{path}/*{n_refs}refs_sc{scenario_id}_k.png'.format(path=path, scenario_id=scenario.id, n_refs=len(scenario.refs))
    return len(glob(pattern)) > 0

def get_image(path, scenario_id, n_refs, k_or_r):
    return glob('{path}/*{n_refs}refs_sc{scenario_id}_{k_or_r}.png'.format(
        path=path,
        scenario_id=scenario_id,
        n_refs=n_refs,
        k_or_r=k_or_r
    ))[0]

def add_preambule(notebook):
    # Preliminary
    notebook.add_code_cell("""
        from IPython.display import display, HTML, Image, Markdown
        from parse import parse_stats_from_file, parse_fits_from_file, summary_from_data
        from base64 import b64encode

        def display_image_side_by_side(*imgs):
            im_html = lambda im: '<img style="display:inline-block; width:50%%" src="data:image/png;base64,%s" />' % b64encode(im.data)
            display(HTML('<div style="display: flex; align-items: flex-end">%s</div>' % ''.join(map(im_html, imgs))))
    """, id='1_preambule')

def add_title(notebook, title):
    notebook.add_code_cell(render("""
        display(HTML("<h1>{{ title }}</h1>"))
    """, title=title), id='4_title')

def exit(msg):
    sys.stderr.write('{0}\n'.format(msg))
    sys.exit(1)


def get_stats_files(data_dir):
    files = glob('{0}/*Stats*.dat'.format(data_dir))
    if len(files) == 0:
        raise ValueError('No refs files in {0}. Your refs files should end with "Stats<number>.dat". example: "S400_T30_C_2refs_LinearStats5.dat"'.format(data_dir))
    return sorted(files)


def get_fit_files(data_dir):
    files = glob('{0}/*Fits*.dat'.format(data_dir))
    if len(files) == 0:
        raise ValueError('No refs files in {0}. Your refs files should end with "Fits<number>.dat". example: "S400_T30_C_2refs_LinearFits5.dat"'.format(data_dir))
    return sorted(files)


def get_names_from_data_dir(data_dir):
    filebase = osp.basename(data_dir if not data_dir.endswith('/') else data_dir[:-1])
    nb_filename = '{0}.ipynb'.format(filebase)
    title = filebase.split('.')[0].replace('_', ' ')
    return nb_filename, title


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir')
    parser.add_argument('--limit-scenarios', default=20)
    parser.add_argument('--overwrite', action='store_true', default=False)
    parser.add_argument('--merge', action='store_true', default=False)
    args = parser.parse_args()

    data_dir = args.data_dir

    if not osp.exists(data_dir):
        raise ValueError('The directory {0} does not exist'.format(data_dir))

    stat_files = get_stats_files(data_dir)
    fit_files = get_fit_files(data_dir)

    nb_filename, title = get_names_from_data_dir(data_dir)

    print 'Title: {0}'.format(title)
    print

    n = Notebook()

    # Main title
    with n.subsection('1_head'):
        add_preambule(n)
        add_title(n, title)


    for i, stat_file in enumerate(sorted(stat_files)):
        fit_file = fit_files[i]
        stats = parse_stats_from_file(stat_file, limit=args.limit_scenarios)
        fits = parse_fits_from_file(fit_file)
        summary = summary_from_data(stats, fits)

        prefix = '_'.join(stat_file.split('_')[:-1]).split('/')[-1]
        images = glob('{0}/{1}*.png'.format(data_dir, prefix))

        n_refs = len(summary.columns) - len(['fit', 'chi2', 'chi2_reduced', 'r2'])

        print 'Stats file: {0}'.format(stat_file)
        print 'Fits file: {0}'.format(fit_file)
        print '- Number of references: {0}'.format(n_refs)
        print '- Total number of scenarios: {0}'.format(stats.shape[0])
        print

        # Summary
        with n.subsection('2_{n_refs}refs'.format(n_refs=n_refs)):
            heading = osp.basename(stat_file).split('_')[-2].split('.')[0].replace('refs', ' references')
            n.add_code_cell(render("""
                stats = parse_stats_from_file('{{ stat_file }}')
                fits = parse_fits_from_file('{{ fit_file }}')
                summary = summary_from_data(stats, fits)
                formatters = {
                    "fit": lambda v: "<a href='#refs_{{n_refs}}_sc_{0:.0f}'>{0}</a>".format(v)
                }
                display(HTML("<h2>{{ heading }}</h2>"))
                display(HTML(summary.to_html(formatters=formatters, escape=False)))
                """,
                stat_file=stat_file,
                fit_file=fit_file,
                start_ref_column=7,
                heading=heading,
                limit_scenarios=args.limit_scenarios,
                n_refs=n_refs
            ), id='1_summary')

            for image in sorted(images):
                fit_number = image.split('_')[-1].split('.png')[0].replace('#0', '')
                with n.subsection('2_sc{fit_number}'.format(fit_number=fit_number)):
                    n.add_code_cell("""
                        summary_row_html = summary[summary['fit'] == float({fit_number})].to_html()
                        display(HTML('<h3 id="refs_{n_refs}_sc_{fit_number}">scenario {fit_number}</h3>') )
                        display(HTML(summary_row_html))
                        display_image_side_by_side(Image('{image}'))
                    """.format(
                        fit_number=fit_number,
                        n_refs=n_refs,
                        image=image,
                    ), id='1_code')
                    n.add_markdown_cell("Notes : ", id='2_notes')


    def write(n, verb):
        n.write(nb_filename)
        call(['jupyter', 'trust', nb_filename]) # sign the notebook
        print colored('{0} {1} ! ✨'.format(nb_filename, verb), 'green')

    already_exists = osp.exists(nb_filename)
    if already_exists:
        if args.overwrite:
            write(n, 'overwritten')
        elif args.merge:
            n1 = Notebook.open(nb_filename)
            n1.merge(n)
            write(n1, 'merged')
        else:
            print colored('{0} already exists. Notebook creation aborted. Use --merge to merge with existing notebook or --overwrite to overwrite it.'.format(nb_filename), 'red')
    else:
        write(n, 'created')

main()
