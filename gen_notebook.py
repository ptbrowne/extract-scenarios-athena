# -*- coding: utf-8 -*-
from IPython.display import display, Image, HTML
from parse import parse_scenarios_from_file
from glob import glob
import os.path as osp
from notebook import Notebook
from jinja2 import Template

n = Notebook()

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

def add_preambule():
    # Preliminary
    n.add_code_cell("""
        from IPython.display import display, HTML, Image, Markdown
        from parse import parse_scenarios_from_file
        from base64 import b64encode

        def display_image_side_by_side(*imgs):
            im_html = lambda im: '<img style="display:inline-block; width:50%%" src="data:image/png;base64,%s" />' % b64encode(im.data)
            display(HTML('<div style="display: flex; align-items: flex-end">%s</div>' % ''.join(map(im_html, imgs))))
    """, id='1_preambule')

def add_selector(ref_files):
    n.add_code_cell(render("""
        display(HTML(\"\"\"
        <div class='noprint refSelect' style="z-index: 1000; padding: 0.5rem; position: fixed; top: 4rem; left: 1rem; background: white; box-shadow: 2px 2px 4px rgba(0,0,0,0.5)">
            {% for ref_file in ref_files %}
                <a href='#{{ ref_file }}'>{{ basename(ref_file) }}</a><br/>
            {% endfor %}
        </div>
        <script type="text/javascript">
            var node = document.querySelector('.refSelect');
            node.parentNode.removeChild(node);
            document.body.appendChild(node)
        </script>\"\"\"))""", ref_files=ref_files, basename=osp.basename), id='3_selector')

def add_title(title):
    n.add_code_cell(render("""
        display(HTML("<h1>{{ title }}</h1>"))
    """, title=title), id='4_title')

def exit(msg):
    sys.stderr.write('{0}\n'.format(msg))
    sys.exit(1)

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir')
    parser.add_argument('--limit-scenarios', default=20)
    parser.add_argument('--force', action='store_true', default=False)
    args = parser.parse_args()

    data_dir = args.data_dir

    if not osp.exists(data_dir):
        exit('The directory {0} does not exist'.format(data_dir))

    ref_files = glob('{0}/*refs.csv'.format(data_dir))
    if len(ref_files) == 0:
        exit('No refs files in {0}. Your refs files should end with "refs.csv". example: "test_LCF_2refs.csv"')

    filebase = osp.basename(data_dir if not data_dir.endswith('/') else data_dir[:-1])
    notebook_filename = '{0}.ipynb'.format(filebase)
    title = filebase.split('.')[0].replace('_', ' ')
    print 'Title: {0}'.format(title)

    with n.subsection('1_head'):
        add_preambule()
        add_selector(ref_files)
        add_title(title=title)

        # Main title

    for ref_file in ref_files:
        scenarios = parse_scenarios_from_file(ref_file, limit=args.limit_scenarios)
        scenarios_with_images = filter(lambda scenario: has_images(data_dir, scenario), scenarios)

        n_refs = len(scenarios[0].refs)

        print 'Reference file: {0}'.format(ref_file)
        print 'Total number of scenarios: {0}'.format(len(scenarios))
        print 'Total number of scenarios with images: {0}'.format(len(scenarios_with_images))
        print 'Number of references: {0}'.format(n_refs)

        # Summary
        with n.subsection('2_{n_refs}refs'.format(n_refs=n_refs)):

            heading = osp.basename(ref_file).split('_')[-1].split('.')[0].replace('refs', ' references')
            n.add_code_cell(render("""
                scenarios = {scenario.id: scenario for scenario in parse_scenarios_from_file('{{ ref_file }}', limit={{limit_scenarios}})}
                display(HTML(\"\"\"
                    <h2 id="{{ ref_file }}">{{ heading }}</h2>
                    <table id="">
                        <tr>
                            <th>Name</th>
                            {% for n in range(n_refs) %}
                                <th>Ref{{n + 1}}</th>
                            {% endfor %}
                            <th>R-factor</th>
                            <th>Chinu</th>
                            <th>R-factor Delta</th>
                        </tr>
                        {% for scenario in scenarios %}
                        <tr>
                            <td><a href="#{{n_refs}}refs_sc{{scenario.id}}">{{scenario.id}}</a></td>
                            {% for n in range(n_refs) %}
                            <td>{{ scenario.refs[n] }}</td>
                            {% endfor %}
                            <td>{{ '%.5f' % scenario.rfactor }}</td>
                            <td>{{ '%.2f' % scenario.chinu }}</td>
                            <td>{{ '%.2f' % scenario.rfactor_delta }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                    \"\"\"))
                """, scenarios=scenarios, ref_file=ref_file, n_refs=n_refs, heading=heading, limit_scenarios=args.limit_scenarios),
                id='1_summary')

            # Each scenario
            for scenario in scenarios_with_images:
                image_k = get_image(data_dir, scenario.id, len(scenario.refs), 'k')
                image_r = get_image(data_dir, scenario.id, len(scenario.refs), 'r')
                data = dict(scenario=scenario, n_refs=n_refs, image_k = image_k, image_r=image_r)
                with n.subsection('2_sc{scenario.id}'.format(scenario=scenario)):
                    n.add_code_cell("""
                        display(HTML('<h2 id="{n_refs}refs_sc{scenario.id}">scenario {scenario.id}</h2>') )
                        scenario = scenarios[{scenario.id}]
                        for ref in scenario.refs:
                            print ref
                        print 'R=', scenario.rfactor
                        display_image_side_by_side(
                            Image('{image_k}'),
                            Image('{image_r}'))
                    """.format(**data), id='1_code')
                    n.add_markdown_cell("Notes : ", id='2_notes')


    def write(n):
        n.write(notebook_filename)
        print '{0} created ! ✨'.format(notebook_filename)

    if osp.exists(notebook_filename) and not args.force:
        if raw_input('Do you want to merge notebook (y for yes) ? ') == 'y':
            print "{0} already exists, merging...".format(notebook_filename)
            n1 = Notebook.open(notebook_filename)
            n1.merge(n)
            write(n1)
        else:
            print 'Aborted..'
    else:
        write(n)

