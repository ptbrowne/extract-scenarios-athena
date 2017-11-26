from IPython.display import display, Image, HTML
from parse import parse_scenarios_from_file
from glob import glob
import os.path as osp
from notebook import Notebook

n = Notebook()

def has_images(scenario):
    return osp.exists('data/test/test_LCF_2refs_sc{0}_k.png'.format(scenario.id))

# Preliminary
n.add_code_cell("""
from IPython.display import display, HTML, Image, Markdown
from parse import parse_scenarios_from_file
from base64 import b64encode

def display_image_side_by_side(*imgs):
    im_html = lambda im: '<img style="display:inline-block; width:50%%" src="data:image/png;base64,%s" />' % b64encode(im.data)
    display(HTML('<div style="display: flex; align-items: flex-end">%s</div>' % ''.join(map(im_html, imgs))))

scenarios = parse_scenarios_from_file('data/test/test_LCF_2refs.csv')
""")

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
    $( document ).ready(code_toggle);
</script>
<button href="javascript:code_toggle()">Toggle Code</button>\"\"\"))
""")


scenarios = parse_scenarios_from_file('data/test/test_LCF_2refs.csv')
scenarios = filter(has_images, scenarios)

# Summary
n.add_code_cell("""
display(HTML(\"\"\"
<table>
    <tr>
        <th>
            Name
        </th>
        <th>
            Ref1
        </th>
        <th>
            Ref2
        </th>
        <th>
            R-factor
        </th>
        <th>
            Chinu
        </th>
        <th>
            Chinu Delta
        </th>
    </tr>
    {0}
</table>
\"\"\"))
""".format('\n'.join(map(lambda scenario: """
<tr>
    <td><a href="#sc{scenario.id}">{scenario.id}</a></td>
    <td>{scenario.refs[0]}</td>
    <td>{scenario.refs[1]}</td>
    <td>{scenario.rfactor:.5f}</td>
    <td>{scenario.chinu:.2f}</td>
    <td>{scenario.chinu_delta:.2f}</td>
</tr>
""".format(scenario=scenario), scenarios))))

# Each scenario
for i, scenario in enumerate(scenarios):
    n.add_code_cell("""
display(HTML('<h1 id="sc{0}">scenario {0}</h1>') )
scenario = scenarios[{0}]
for ref in scenario.refs:
    print ref
print 'R=', scenario.rfactor
display_image_side_by_side(
    Image('data/test/test_LCF_2refs_sc{0}_k.png'),
    Image('data/test/test_LCF_2refs_sc{0}_r.png') )
""".format(i))
    n.add_markdown_cell("Notes : ")

n.write('tutu.ipynb')

