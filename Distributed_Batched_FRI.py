from common import *

class Distributed_Batched_FRI:
    def __init__(self, circuit_size, number_of_queries, blowup_factor, number_of_bits_per_field_elem, min_S, max_S):
        self.N = circuit_size
        self.l = number_of_queries
        self.blowup_factor = blowup_factor
        self.number_of_bytes_per_field_elem = number_of_bits_per_field_elem / NUMBER_OF_BITS_PER_BYTE
        if min_S < 1:
            raise ValueError("min_S must be at least 1")
        self.min_S = min_S
        if max_S < 1:
            raise ValueError("max_S must be at least 1")
        self.max_S = max_S


    def communication_cost_in_GB(self, M, S):
        T = self.N // M
        K = T / S  # degree bound of each local polynomial

        cost_1 = S * M + M  #  Step 1 + 2: Merkle commitments + random challenge
        cost_2 = M * self.blowup_factor * K  # Step 3: send partially combined evaluation vector to master 
        cost_3 = self.l * M + self.l * M * (S + S * log(K * self.blowup_factor))  # Step 6: batched FRI combination check
        total_cost = cost_1 + cost_2 + cost_3
        cost_in_GB = (total_cost * self.number_of_bytes_per_field_elem) / 10**9

        print("Communication Costs:")
        print(f'Step 1+2 costs {cost_1 / total_cost:.5f}')
        print(f'Step 3 costs {cost_2 / total_cost:.5f}')
        print(f'Step 6 costs {cost_3 / total_cost:.5f}')
        print(f'Total communication cost in GB: {cost_in_GB:.3f} GB')

        return cost_in_GB
    

    def proof_size_in_GB(self, M, S):
        T = self.N // M
        K = T / S  # degree bound of each local polynomial
        number_of_folding_rounds = log(K) - log(self.blowup_factor)

        cost_1 = S * M  # Step 1: commitments of all unbatched polynomials
        cost_2 = number_of_folding_rounds  # Step 5: batched FRI proof folding phase 
        cost_2 += self.l * 2 * number_of_folding_rounds * (1 + log(K * self.blowup_factor))  # Step 5: batched FRI proof query phase
        cost_3 = self.l * M * (S + S * log(K * self.blowup_factor)) # Step 6: batched FRI combination check
        total_cost = cost_1 + cost_2 + cost_3
        cost_in_GB = (total_cost * self.number_of_bytes_per_field_elem) / 10**9

        print("Proof size:")
        print(f'Step 1 costs {cost_1 / total_cost:.5f}')
        print(f'Step 5 costs {cost_2 / total_cost:.5f}')
        print(f'Step 6 costs {cost_3 / total_cost:.5f}')
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
    instance = Distributed_Batched_FRI(circuit_size=2**35, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, min_S=1, max_S=2**50)
    # instance = Distributed_Batched_FRI(circuit_size=2**30, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, min_S=15, max_S=50)
    # instance = Distributed_Batched_FRI(circuit_size=2**40, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, min_S=40, max_S=300)
    # instance = Distributed_Batched_FRI(circuit_size=2**50, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, min_S=50, max_S=400)
    instance.plot_communication_cost()
    instance.plot_proof_size()
