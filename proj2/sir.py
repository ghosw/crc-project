import enum
import networkx as nx
import networkx.classes
import networkx.classes.function
import numpy as np
import sys


class SirState(enum.Enum):
    SUSCEPTIBLE = 1
    INFECTED = 2
    RECOVERED = 3
    VACCINATED = 4

class Sir(object):
    def __init__(self, g, beta, f=0, seed=None):
        if seed:
            np.random.seed(seed)

        self._state = 'state'
        self.g = g
        self.beta = beta
        self.f = f
        self._num_s_i_edges = None
        self._infected_nodes = None
        self._infected_node_edges = None
        self._iterations_info = None

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, g):
        self._g = g

    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, beta):
        if not 0 <= beta <= 1:
            raise ValueError(
                'beta should be a proportion (0 <= beta <= 1)'
            )
        
        self._beta = beta

    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, f):
        if not 0 <= f <= 1:
            raise ValueError(
                'f should be a proportion (0 <= f <= 1)'
            )

        self._f = f

    def _initialize_sir_network(self):
        nx.classes.function.set_node_attributes(
            self._g, 
            SirState.SUSCEPTIBLE, 
            self._state
        )

        self._vaccinate_before_sim()
        self._iterations_info = []
        aux = self._first_infect_event()
        self._infected_node_edges, self._num_s_i_edges = *aux
        self._infected_nodes = list(self._infected_node_edges.keys())

    def _first_infect_event(self):
        node_to_infect = np.random.randint(0, len(self._g))
        self._g.nodes[node_to_infect][self._state] = SirState.INFECTED
        s_i_edges = self._neighbour_s_i_edges(node_to_infect)
        return {node_to_infect: s_i_edges}, len(s_i_edges)

    def _vaccinate_before_sim(self):
        for _ in range(int(round(len(self._g) * self._f))):
            node = np.random.randint(0, len(g))
            self._g.nodes[node][self._state] = SirState.VACCINATED

    def simulate(self):
        self._initialize_sir_network()

        while self._infected_nodes:
            inf_r = self._beta * self._num_s_i_edges
            time_inc_r = 1 / (inf_r + len(self._infected_nodes))
            prob_to_infect = inf_r / (inf_r + len(self._infected_nodes))
            self._check_new_iteration(time_inc_r)
            self._perform_infection_or_recovery_event(prob_to_infect)

        self._save_simulation()

    def _check_new_iteration(self, time_inc_ratio):
        if np.random.uniform() < time_inc_ratio:
            self._iterations_info.append([
                self._iterations_info[-1][0], 
                self._iterations_info[-1][1]
            ])

    def _perform_infection_or_recovery_event(self, prob_to_infect):
        if np.random.uniform() < prob_to_infect:
            self._iterations_info[-1][1] += 1
            self._iterations_info[-1][0] -= 1
            self._infect_event()
        else:
            self._iterations_info[-1][1] -= 1
            self._recover_event()

    def _infect_event(self):
        infected_node, node_to_infect = self._select_s_i_edge()
        self._g.nodes[node_to_infect][self._state] = SirState.INFECTED
        self._infected_nodes.append(node_to_infect)
        new_s_i_edges = _neighbour_s_i_edges(node_to_infect)
        self._infected_node_edges[node_to_infect] = new_s_i_edges
        removed_s_i_edges = _rm_s_i_edges_of_new_infected(
            node_to_infect, 
        )

        self._num_s_i_edges += (-removed_s_i_edges + len(new_s_i_edges))

    def _recover_event(self):
        rec_node_idx = np.random.randint(0, len(self._infected_nodes))
        node_to_recover = self._infected_nodes.pop(rec_node_idx)
        g.nodes[node_to_recover][self._state] = SirState.RECOVERED
        rem_edges = self._infected_node_edges.pop(node_to_recover, None)
        self._num_s_i_edges -= len(rem_edges)

    def _rm_s_i_edges_of_new_infected(self, inf_node):
        edges_removed = 0

        for neigh in g.neighbors(inf_node):
            if g.nodes[neigh][self._state] != SirState.INFECTED:
                continue

            inf_node_links = self._infected_node_edges[neigh]

            for idx in range(len(inf_node_links) - 1, -1, -1): 
                if (inf_node_links[idx] == inf_node):
                    inf_node_links.pop(idx)
                    edges_removed += 1
                    break

        return edges_removed

    def _select_s_i_edge(self):
        i = np.random.randint(0, self._num_s_i_edges)
        edge_count = 0

        for node in self._infected_node_edges:
            lcl_edge_count = len(self._infected_node_edges[node])
            
            if lcl_edge_count <= 0:
                continue
                
            if i >= edge_count + lcl_edge_count:
                edge_count += lcl_edge_count
                continue

            return node, self._infected_node_edges[node][i - edge_count]

    def _neighbour_s_i_edges(self, node):
        s_i_edges = []

        for edge in g.edges(node):
            if g.nodes[edge[0]][self._state] == SirState.SUSCEPTIBLE:
                s_i_edges.append(edge[0])
            elif g.nodes[edge[1]][self._state] == SirState.SUSCEPTIBLE:
                s_i_edges.append(edge[1])

        return s_i_edges


def _max_infected(report):
    max_val = -1

    for it in report:
        if it[1] > max_val:
            max_val = it[1]

    return max_val

if __name__ == '__main__':
    print(*sys.argv)

    sims = []
    n = int(sys.argv[1])
    m = int(sys.argv[3])
    
    for _ in range(m):
        sims.append(sir_simulation(nx.barabasi_albert_graph(n, 2), float(sys.argv[2])))
    
    cum_infected_frac = 0

    for report in sims:
        cum_infected_frac += (n - _max_infected(report)) / n

    print(cum_infected_frac / m)
