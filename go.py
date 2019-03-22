import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DIR, 'deps'))

import djangogo

parser = djangogo.make_parser()
parser.add_argument('--run-frontend', '-f', action='store_true')
args = parser.parse_args()

if args.run_frontend:
    djangogo.invoke('npm', 'run', 'serve')
else: djangogo.main(args,
    project='dnd_weave_proj',
    app='dnd_weave_app',
    db_name='dnd_weave_database',
    db_user='dnd_weave_user',
    heroku_url='https://dnd-weave.herokuapp.com/',
)
