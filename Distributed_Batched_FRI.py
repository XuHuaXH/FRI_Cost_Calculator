from common import *

class Distributed_Batched_FRI:
    def __init__(self, circuit_size, num_of_queries, blowup_factor, field_elem_size, min_S, max_S):
        self.N = circuit_size
        self.l = num_of_queries
        self.blowup_factor = blowup_factor
        self.field_elem_size = field_elem_size
        self.num_bytes_per_elem = field_elem_size / 8
        self.min_S = 1
        if min_S < 1:
            raise ValueError("min_K must be at least 1")
        self.min_S = min_S
        if max_S < 1:
            raise ValueError("max_K must be at least 1")
        self.max_S = max_S

    def communication_cost_in_GB(self, M, S):
        T = self.N / M
        K = T / S  # deg_per_polynomial

        print("Communication Costs:")
        cost_1 = S * M + M  #  cost: Merkle commitments + random challenge
        cost_2 = M * self.blowup_factor * K  # cost: send partially combined eval vector to master 
        cost_3 = self.l * M * (S + S * log(K))  # cost: batched FRI combination check
        total_cost = cost_1 + cost_2 + cost_3

        print(f'Step 1 costs {cost_1 / total_cost:.5f}')
        print(f'Step 2 costs {cost_2 / total_cost:.5f}')
        print(f'Step 3 costs {cost_3 / total_cost:.5f}')
        cost_in_GB = (total_cost * self.num_bytes_per_elem) / 10**9
        print(f'Total communication cost in GB: {cost_in_GB:.3f} GB')

        return cost_in_GB
    
    def proof_size_in_GB(self, M, S):
        T = self.N / M
        K = T / S  # deg_per_polynomial

        print("Proof size:")
        cost_1 = S * M  # Step 1: commitments of all unbatched polynomials
        cost_2 = log(K)  # Step 2: batched FRI proof folding phase 
        cost_2 += self.l * 2 * log(K) * (1 + log(K))  # Step 2: batched FRI proof query phase
        cost_3 = self.l * M * (S + S * log(K)) # Step 3: batched FRI combination check
        total_cost = cost_1 + cost_2 + cost_3

        print(f'Step 1 costs {cost_1 / total_cost:.5f}')
        print(f'Step 2 costs {cost_2 / total_cost:.5f}')
        print(f'Step 3 costs {cost_3 / total_cost:.5f}')
        cost_in_GB = (total_cost * self.num_bytes_per_elem) / 10**9
        print(f'Proof size in GB: {cost_in_GB:.3f} GB')

        return cost_in_GB
    
    def plot_communication_cost(self):
        fig = go.Figure()
        fig.update_layout(title="Communication Cost for Distributed Batched FRI", legend_title_text = "Number of Machines")
        fig.update_xaxes(title_text="Num of polynomials per node S")
        fig.update_yaxes(title_text="Comm. Cost in GB")

        for M in [2 ** i for i in range(9)]:
            T = self.N // M
            x = []
            y = []
            for S in range(min(T, self.min_S), min(T, self.max_S), min(T, self.max_S) // 20):
                x.append(S)
                y.append(self.communication_cost_in_GB(M=M, S=S))
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers+lines', name=f'{M}'))
        
        fig.show(config={'scrollZoom': True})


    def plot_proof_size(self):
        fig = go.Figure()
        fig.update_layout(title="Proof Size for Distributed Batched FRI", legend_title_text = "Number of Machines")
        fig.update_xaxes(title_text="Num of polynomials per node S")
        fig.update_yaxes(title_text="Proof Size in GB")

        for M in [2 ** i for i in range(9)]:
            T = self.N // M
            x = []
            y = []
            for S in range(min(T, self.min_S), min(T, self.max_S), min(T, self.max_S) // 20):
                x.append(S)
                y.append(self.proof_size_in_GB(M=M, S=S))
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers+lines', name=f'{M}'))
        
        fig.show(config={'scrollZoom': True})


if __name__ == "__main__":
    instance = Distributed_Batched_FRI(circuit_size=2**50, num_of_queries=350, blowup_factor=8, field_elem_size=256, min_S=1, max_S=600)
    instance.plot_communication_cost()
    instance.plot_proof_size()
