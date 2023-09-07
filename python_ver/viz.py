from dash import Dash, dcc, html, Output, Input, State, callback, exceptions
import dash_bootstrap_components as dbc
import dash_latex as dl
import visdcc
from util import tex_matrix
from markov import Markov
import const
import pandas as pd
import numpy as np

# Init
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

DEFAULT_STATES = ['McDonalds', 'TacoBell', 'InNOut', 'KFC']
DEFAULT_ITERS = 1000
DEFAULT_TRANSITIONS = [
    [0.1, 0.2, 0, 0.7],  # Mcd's
    [0.25, 0.25, 0.5, 0],  # TB's
    [0, 0.2, 0.8, 0],  # InOut's
    [0.3, 0.5, 0, 0.2],  # KFC's
]

# Interface
input_state_list = html.Div(
    [
        dbc.Label("States:", html_for="example-email"),
        dbc.Textarea(id='input_states', className="mb-3", placeholder="Enter Distinct MC States",
                     value='\n'.join(DEFAULT_STATES)),
        dbc.FormText(
            "Enter a list of state names separated by whitespace.",
            color="secondary",
        ),
    ],
    className="mb-3",
)

input_iterations = html.Div(
    [
        dbc.Label("Iterations", html_for="example-email"),
        dbc.Input(id='input_iter', className="mb-3", placeholder="Enter # of Iterations",
                  value=DEFAULT_ITERS),
    ],
    className="mb-3",
)

input_transition_matrix = html.Div(
    [
        dbc.Label("Transition Matrix", html_for="example-email"),
        dbc.Textarea(id='input_tmat', className="mb-3", placeholder="Enter Distinct MC States",
                     value='\n'.join([' '.join([str(y) for y in x]) for x in DEFAULT_TRANSITIONS])),
        dbc.FormText(
            "Provide the entries of the transition matrix at t=0. Separate each entry by whitespace.",
            color="secondary",
        ),
    ],
    className="mb-3",
)

markov_chain = visdcc.Network(
    id='net',
    data={'nodes': dict(), 'edges': dict(), 'interaction': const.INTERACT, 'physics': const.PHYSICS},
    options=dict(height='450px', width='100%')
)

# Layout
# TODO: frontend pretty
app.layout = dbc.Container([
    dcc.Markdown(id='main_head', children="# Markov Chain Visualizer"),
    dbc.Row([
        dbc.Col([
            markov_chain,
            dcc.Markdown(id='lbl-cur', children="## **Current State:**"),
            dbc.Row(
                [
                    dbc.Col([
                        dcc.Markdown(children="Step between states:"),
                        dbc.ButtonGroup(
                            [
                                dbc.Button("<<", id='btn_rw', n_clicks=0, disabled=True),
                                dbc.Button(">>", id='btn_ff', n_clicks=0, disabled=True)
                            ],
                            size="lg", className="me-1")], width=4),
                    dbc.Col([
                        dcc.Markdown(children="Simulation Frame:"),
                        dcc.Slider(0, 1000, 1, value=0, marks=None, id='frame_slider',
                                   tooltip={"placement": "bottom", "always_visible": True},
                                   disabled=True)], width=8),
                ],
                className='pb-4'),
        ]),
        dbc.Col([
            dcc.Markdown(children="## Specify Markov Chain:"),
            input_state_list,
            input_iterations,
            input_transition_matrix,
            dbc.Button("Confirm", id='btn_confirm', color="primary", className="me-1", n_clicks=0),
        ]),
    ], className='pb-4'),
    dbc.Row([
        dcc.Markdown(children="### Observed State Frequencies:"),
        dl.DashLatex(id='lbl-obs-freq', children=""),
        dcc.Markdown(children="### Observed State Probabilities:"),
        dl.DashLatex(id='lbl-obs-prob', children=""),
        dcc.Markdown(children="### Theoretical n-th State Probabilities:"),
        dl.DashLatex(id='lbl-thr-prob', children=""),
        dcc.Markdown(children="### Theoretical n-th Transition Matrix P(j = current_state | i = start_state):"),
        dl.DashLatex(id='lbl-thr-tm', children=""),
        dcc.Markdown(children="### Theoretical Stationary Distribution:"),
        dl.DashLatex(id='lbl-thr-std', children=""),
    ]),
    dcc.Store(id='cur-state', data=0),
    dcc.Store(id='cur-step', data=0),
    dcc.Store(id='max-step'),
    dcc.Store(id='sequence', data=[]),
    dcc.Store(id='state-names', data=[]),

    dcc.Store(id='obs-freq', data=[]),
    dcc.Store(id='obs-prob', data=[]),
    dcc.Store(id='thr-prob', data=[]),
    dcc.Store(id='thr-mat', data=[]),
    dcc.Store(id='thr-std', data=[]),

    dcc.Store(id='chain-nodes', data=[]),
    dcc.Store(id='chain-edges', data=[]),
],
    style={
        "padding": "20px"
    })


@callback(
    Output(markov_chain, 'data', allow_duplicate=True),
    Output('frame_slider', 'value', allow_duplicate=True),
    Output('chain-nodes', 'data', allow_duplicate=True),
    Output('chain-edges', 'data', allow_duplicate=True),
    Output('lbl-cur', 'children', allow_duplicate=True),

    Output('obs-freq', 'data'),
    Output('obs-prob', 'data'),
    Output('thr-prob', 'data'),
    Output('thr-mat', 'data'),
    Output('thr-std', 'data'),

    Output('state-names', 'data'),
    Output('max-step', 'data'),
    Output('sequence', 'data'),
    Output('cur-state', 'data'),
    Output('cur-step', 'data'),

    Output('frame_slider', 'disabled'),
    Output('frame_slider', 'max'),
    Output('btn_rw', 'disabled'),
    Output('btn_ff', 'disabled'),

    Input('btn_confirm', 'n_clicks'),
    State('input_states', 'value'),
    State('input_iter', 'value'),
    State('input_tmat', 'value'),
    prevent_initial_call=True
)
def markov_create(_, states, iters, t_mat):
    # Clean MC parameters
    # TODO: validate data is string
    states = states.split()

    # TODO: validate data is valid int
    states_ct = len(states)
    iters = int(iters)

    transitions_split = [float(i) for i in t_mat.split()]
    # TODO: assert t_mat is stochastic row-wise *important
    t_mat = np.array([transitions_split[i:i + states_ct] for i in
                     range(0, len(transitions_split), states_ct)])

    chain = Markov(states, iters, t_mat)
    max_step = len(chain.sequence) - 1

    # Sorry
    # {'nodes': chain.nodes, 'edges': chain.edges, 'interaction': const.INTERACT, 'physics': const.PHYSICS}
    return {'nodes': chain.nodes, 'edges': chain.edges}, \
        0, chain.nodes, chain.edges, \
        "**Current State: **" + states[0], \
        chain.obs_state_frequencies, chain.obs_state_probs, chain.theory_state_probs, \
        chain.theory_transitions, chain.stationary_dist, \
        states, max_step, chain.sequence, 0, 0, \
        False, max_step, False, False


@callback(
    Output('cur-state', 'data', allow_duplicate=True),
    Output('cur-step', 'data', allow_duplicate=True),
    Output("frame_slider", 'value', allow_duplicate=True),
    State('cur-step', 'data'),
    State('sequence', 'data'),
    Input('btn_rw', 'n_clicks'),
    prevent_initial_call=True
)
def mc_prev(pv_step, seq, _):
    if pv_step > 0:
        return seq[pv_step - 1], pv_step - 1, pv_step - 1
    raise exceptions.PreventUpdate


@callback(
    Output('cur-state', 'data', allow_duplicate=True),
    Output('cur-step', 'data', allow_duplicate=True),
    Output("frame_slider", 'value', allow_duplicate=True),
    State('cur-step', 'data'),
    State('max-step', 'data'),
    State('sequence', 'data'),
    Input('btn_ff', 'n_clicks'),
    prevent_initial_call=True
)
def mc_next(pv_step, max_step, seq, _):
    if pv_step < max_step:
        return seq[pv_step + 1], pv_step + 1, pv_step + 1
    raise exceptions.PreventUpdate


@callback(
    Output('cur-step', 'data', allow_duplicate=True),
    Input('frame_slider', 'value'),
    prevent_initial_call=True
)
def slider_state(val):
    return val


@callback(
    Output(markov_chain, 'data', allow_duplicate=True),
    Output('lbl-cur', 'children', allow_duplicate=True),

    Output('lbl-obs-freq', 'children', allow_duplicate=True),
    Output('lbl-obs-prob', 'children', allow_duplicate=True),
    Output('lbl-thr-prob', 'children', allow_duplicate=True),
    Output('lbl-thr-tm', 'children', allow_duplicate=True),
    Output('lbl-thr-std', 'children', allow_duplicate=True),

    State('state-names', 'data'),
    State('chain-nodes', 'data'),
    State('chain-edges', 'data'),

    State('obs-freq', 'data'),
    State('obs-prob', 'data'),
    State('thr-prob', 'data'),
    State('thr-mat', 'data'),
    State('thr-std', 'data'),

    State('sequence', 'data'),

    Input('cur-step', 'data'),
    prevent_initial_call=True
)
def update_chain(
        states, nodes, edges,
        obs_freq, obs_prob, thr_prob, thr_mat, thr_stationary_dist,
        sequence,
        cur_step):
    new_state_idx = sequence[cur_step]
    new_state = states[new_state_idx]

    obs_freq_tex = tex_matrix(obs_freq[cur_step])
    obs_prob_tex = tex_matrix(obs_prob[cur_step])
    thr_prob_tex = tex_matrix(thr_prob[cur_step])
    thr_mat_tex = tex_matrix(thr_mat[cur_step], vector=False)
    thr_std_tex = tex_matrix(thr_stationary_dist)

    print(thr_stationary_dist)
    print(thr_std_tex)

    for node in nodes:
        node['color'] = const.NODE_COLOR_IDLE
    nodes[new_state_idx]['color'] = const.NODE_COLOR_ACTIVE

    return {'nodes': nodes, 'edges': edges, 'interaction': const.INTERACT, 'physics': const.PHYSICS}, \
        "## **Current State: **" + new_state, \
        obs_freq_tex, obs_prob_tex, thr_prob_tex, thr_mat_tex, thr_std_tex


if __name__ == '__main__':
    app.run_server(debug=True)
