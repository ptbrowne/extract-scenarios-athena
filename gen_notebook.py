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

def has_images(scenario):
    return osp.exists('data/test/test_LCF_2refs_sc{0}_k.png'.format(scenario.id))

def add_preambule():
    # Preliminary
    n.add_code_cell("""
        from IPython.display import display, HTML, Image, Markdown
        from parse import parse_scenarios_from_file
        from base64 import b64encode

        def display_image_side_by_side(*imgs):
            im_html = lambda im: '<img style="display:inline-block; width:50%%" src="data:image/png;base64,%s" />' % b64encode(im.data)
            display(HTML('<div style="display: flex; align-items: flex-end">%s</div>' % ''.join(map(im_html, imgs))))
    """)

def add_toggle_code():
    n.add_code_cell("""
        display(HTML(\"\"\"<script>
            var code_show=true; //true -> hide code at first

            function code_toggle () {
                $('div.prompt').hide(); // always hide prompt
                if (code_show){
                    $('div.input').hide();
                } else {
                    $('div.input').show();
                }
                code_show = !code_show
            }
            $(document).ready(code_toggle);
        </script>
        <style>
        @media print {
          .noprint { display: none }
        }
        </style>
        <button class='noprint' onclick="javascript:code_toggle()">Toggle Code</button>\"\"\"))
    """)

def exit(msg):
    sys.stderr.write('{0}\n'.format(msg))
    sys.exit(1)

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir')
    parser.add_argument('--limit-scenarios', default=20)
    args = parser.parse_args()

    data_dir = args.data_dir

    if not osp.exists(data_dir):
        exit('The directory {0} does not exist'.format(data_dir))

    ref_files = glob('{0}/*refs.csv'.format(data_dir))
    if len(ref_files) == 0:
        exit('No refs files in {0}. Your refs files should end with "refs.csv". example: "test_LCF_2refs.csv"')

    add_preambule()
    add_toggle_code()

    # Reference selector
    n.add_code_cell(render("""
        display(HTML(\"\"\"
        <div class='noprint refSelect' style="z-index: 1000; padding: 0.5rem; position: fixed; top: 4rem; left: 1rem; background: white; box-shadow: 2px 2px 4px rgba(0,0,0,0.5)">
            {% for ref_file in ref_files %}
                <a href='#{{ ref_file }}'>{{ osp.basename(ref_file) }}</a><br/>
            {% endfor %}
        </div>
        <script type="text/javascript">
            var node = document.querySelector('.refSelect');
            node.parentNode.removeChild(node);
            document.body.appendChild(node)
        </script>\"\"\"))""", ref_files=ref_files, osp=osp))

    # Main title
    notebook_filename = '{0}.ipynb'.format(osp.basename(data_dir[:-1]))
    n.add_code_cell(render("""
        display(HTML("<h1>{{ notebook_filename }}</h1>"))
    """, notebook_filename=notebook_filename))

    for ref_file in ref_files:
        scenarios = parse_scenarios_from_file(ref_file, limit=args.limit_scenarios)
        scenarios_with_images = filter(has_images, scenarios)

        n_refs = len(scenarios[0].refs)

        print 'Reference file: {0}'.format(ref_file)
        print 'Total number of scenarios: {0}'.format(len(scenarios))
        print 'Total number of scenarios with images: {0}'.format(len(scenarios_with_images))
        print 'Number of references: {0}'.format(n_refs)

        # Summary
        title = osp.basename(ref_file).split('_')[-1].split('.')[0]
        n.add_code_cell(render("""
            scenarios = parse_scenarios_from_file('{{ ref_file }}')
            display(HTML(\"\"\"
                <h2 id="{{ ref_file }}">{{ title }}</h2>
                <table id="">
                    <tr>
                        <th>
                            Name
                        </th>
                        {% for n in range(n_refs) %}
                            <th>
                                Ref{{n + 1}}
                            </th>
                        {% endfor %}
                        <th>
                            R-factor
                        </th>
                        <th>
                            Chinu
                        </th>
                        <th>
                            R-factor Delta
                        </th>
                    </tr>
                    {% for scenario in scenarios %}
                    <tr>
                        <td><a href="#sc{{scenario.id}}">{{scenario.id}}</a></td>
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
            """, scenarios=scenarios, ref_file=ref_file, n_refs=n_refs, title=title))

        # Each scenario
        for i, scenario in enumerate(scenarios_with_images):
            n.add_code_cell("""
                display(HTML('<h2 id="sc{0}">scenario {0}</h2>') )
                scenario = scenarios[{0}]
                for ref in scenario.refs:
                    print ref
                print 'R=', scenario.rfactor
                display_image_side_by_side(
                    Image('data/test/test_LCF_2refs_sc{0}_k.png'),
                    Image('data/test/test_LCF_2refs_sc{0}_r.png') )
        """.format(i))
            n.add_markdown_cell("Notes : ")

    n.write(notebook_filename)
    print '{0} created ! ✨'.format(notebook_filename)

