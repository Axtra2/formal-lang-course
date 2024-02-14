import cfpq_data
import networkx.drawing.nx_pydot


def get_graph_info(name):
    path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(path)
    return (graph.number_of_nodes(), graph.number_of_edges(), graph.edges(data=True))


def labeled_two_cycles_graph_to_dot(n, m, labels, path):
    if labels is None:
        g = cfpq_data.labeled_two_cycles_graph(n, m)
    else:
        g = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    networkx.drawing.nx_pydot.write_dot(g, path)
