
import networkx as nx
import plotly.graph_objects as go


class Graph_Viz_Engine:

    def __init__(
        
        self,
        graph: nx.Graph,
        pos: dict,
        node_cmap: dict = None,
        auto: bool = True
        
        ) -> None:

        self.graph = graph
        self.pos = pos
        self.node_cmap = node_cmap
        self.edges = {
            'x': [],
            'y': []
        }
        self.nodes = {
            'x': [],
            'y': []
        }

        self.run(auto=auto)


    def run(self, auto: bool) -> None:

        if auto:
            self.automation_engine()

    def build_edge_vectors(self) -> None:

        for e in self.graph.edges():

            x0, y0 = self.pos[e[0]]
            x1, y1 = self.pos[e[1]]

            self.edges['x'].extend([x0, x1, None])
            self.edges['y'].extend([y0, y1, None])

    def build_edge_sets(self, filter_nodes: list = None) -> None:

        if filter_nodes is None:
            filter_nodes = list(self.node_cmap.keys())

        self.edge_traces = []

        for node in self.graph.nodes:
            if node in filter_nodes:

                edge_set = nx.edges(self.graph, [node])
                e_x, e_y = [], []
                for e in edge_set:

                    x0, y0 = self.pos[e[0]]
                    x1, y1 = self.pos[e[1]]

                    e_x.extend([x0, x1, None])
                    e_y.extend([y0, y1, None])

                    self.edge_traces.append(
                        go.Scatter(
                            x=e_x,
                            y=e_y,
                            line={
                                "width": 0.5,
                                "color": self.node_cmap[node]
                            },
                            hoverinfo='text',
                            text=[f"{e[0]} --> {e[1]}"],
                            mode='lines'
                        )
                    )


    def set_edge_trace(self) -> None:

        self.edge_trace = go.Scatter(

            x=self.edges['x'],
            y=self.edges['y'],
            line={
                'width': 0.8,
                'color': '#888'
            },
            hoverinfo='text',
            text=list(self.graph.edges()),
            mode='lines'
        )

    def build_node_vectors(self) -> None:

        for n in self.graph.nodes():

            x, y = self.pos[n]
            self.nodes['x'].append(x)
            self.nodes['y'].append(y)

    def set_node_trace(self) -> None:

        self.node_trace = go.Scatter(

            x=self.nodes['x'],
            y=self.nodes['y'],
            mode='markers',
            hoverinfo='text',
            marker={
                'color':[],
                'size': 10,
            }
        )

    def set_node_details(self) -> None:

        node_color, node_text, node_size = [], [], []

        for node in self.graph.nodes():

            if node in list(self.node_cmap.keys()):
                color = self.node_cmap[node]

            else:
                color = "black"

            ns = len(list(self.graph.neighbors(node)))
            node_color.append(color)
            node_text.append(f" {node} ---> {ns} connections")
            node_size.append(ns)
            

        self.node_trace.marker.color = node_color
        self.node_trace.text = node_text
        # self.node_trace.marker.size = node_size


    def build_figure(self, filtered: bool = False) -> None:

        if filtered:
            data = self.edge_traces + [self.node_trace]

        else:
            data = [
                self.edge_trace,
                self.node_trace
            ]

        self.fig = go.Figure(

            data=data,
            layout=go.Layout(
                template="plotly_white",
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin={
                    'b': 20,
                    'l': 5,
                    'r': 5,
                    't': 40
                },
                annotations=[
                    {   
                        'text': 'outbound requests snapshot',
                        'showarrow': False,
                        'xref': 'paper',
                        'yref': 'paper',
                        'x' :0.005,
                        'y': 0.002
                    }
                ],
                xaxis={
                    'showgrid': False,
                    'zeroline': False,
                    'showticklabels': False
                },
                yaxis={
                    'showgrid': False,
                    'zeroline': False,
                    'showticklabels': False
                },
                height=800,
                width=800
            )
        )


    def automation_engine(self) -> None:

        self.build_edge_vectors()
        self.set_edge_trace()

        self.build_node_vectors()
        self.set_node_trace()
        self.set_node_details()

        self.build_figure()