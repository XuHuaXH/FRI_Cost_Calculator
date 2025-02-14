from common import *

class Fold_and_Batch:
    def __init__(self, circuit_size, num_of_queries, blowup_factor, field_elem_size, max_K):
        self.N = circuit_size
        self.l = num_of_queries
        self.blowup_factor = blowup_factor
        self.field_elem_size = field_elem_size
        self.num_bytes_per_elem = field_elem_size / 8
        self.min_K = blowup_factor
        if max_K < blowup_factor:
            raise ValueError("max_K must be larger than the blowup factor!")
        self.max_K = max_K


    def communication_cost_in_GB(self, M, K):
        T = self.N / M

        cost_1 = M  # Step 1: Merkle commitments of all local polynomials
        cost_2 = M * log(T / K)  # Step 3: Merkle commitments of local intermediate folded polynomials
        cost_3 = M  # Step 4: sending random challenge to all worker nodes
        cost_4 = M * self.blowup_factor * K  # Step 5: workers sending partially folded local polynomials
        cost_5 = self.l * M + self.l * M * 2 * log(T / K) * (1 + log(T))  # Step 8: folding checks for local folding
        total_cost = cost_1 + cost_2 + cost_3 + cost_4 + cost_5
        
        print(f'Step 1 costs {cost_1 / total_cost:.5f}')
        print(f'Step 3 costs {cost_2 / total_cost:.5f}')
        print(f'Step 4 costs {cost_3 / total_cost:.5f}')
        print(f'Step 5 costs {cost_4 / total_cost:.5f}')
        print(f'Step 8 costs {cost_5 / total_cost:.5f}')
        cost_in_GB = (total_cost * self.num_bytes_per_elem) / 10**9
        print(f'Total communication in GB: {cost_in_GB:.3f} GB')

        return cost_in_GB


    def proof_size_in_GB(self, M, K):
        T = self.N / M

        print("Proof size:")
        cost_1 = M  # Step 1: commitments of all local polynomials
        cost_2 = M * log(T / K)  # Step 3: Merkle commitments of locally folded polynomials  
        cost_3 = log(K)  # Step 7: FRI proof folding phase for G(X)
        cost_4 = self.l * M * 2 * log(T / K) * (1 + log(T))  # Step 8: folding checks for local folding
        cost_5 = self.l * 2 * log(K) * (1 + log(K))  # Step 9: folding checks for batched folding
        total_cost = cost_1 + cost_2 + cost_3 + cost_4 + cost_5

        print(f'Step 1 costs {cost_1 / total_cost:.5f}')
        print(f'Step 3 costs {cost_2 / total_cost:.5f}')
        print(f'Step 7 costs {cost_3 / total_cost:.5f}')
        print(f'Step 8 costs {cost_4 / total_cost:.5f}')
        print(f'Step 9 costs {cost_5 / total_cost:.5f}')
        cost_in_GB = (total_cost * self.num_bytes_per_elem) / 10**9
        print(f'Proof size in GB: {cost_in_GB:.3f} GB')

        return cost_in_GB


    def plot_communication_cost(self):
        fig = go.Figure()
        fig.update_layout(title="Communication Cost for Fold-and-Batch", legend_title_text = "Number of Machines")
        fig.update_xaxes(title_text="Folding Parameter K")
        fig.update_yaxes(title_text="Comm. Cost in GB")

        for M in [2 ** i for i in range(9)]:
            T = self.N // M
            x = []
            y = []
            for K in range(self.min_K, min(T, self.max_K), min(T, self.max_K) // 20):
                x.append(K)
                y.append(self.communication_cost_in_GB(M=M, K=K))
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers+lines', name=f'{M}' ))

        fig.show(config={'scrollZoom': True})


    def plot_proof_size(self):
        fig = go.Figure()
        fig.update_layout(title="Proof Size for Fold-and-Batch", legend_title_text = "Number of Machines")
        fig.update_xaxes(title_text="Folding Parameter K")
        fig.update_yaxes(title_text="Proof Size in GB")

        for M in [2 ** i for i in range(9)]:
            T = self.N // M
            x = []
            y = []
            for K in range(self.min_K, min(T, self.max_K), min(T, self.max_K) // 20):
                x.append(K)
                y.append(self.proof_size_in_GB(M=M, K=K))
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers+lines', name=f'{M}'))
        
        fig.show(config={'scrollZoom': True})





if __name__ == "__main__":
    instance = Fold_and_Batch(circuit_size=2**50, num_of_queries=350, blowup_factor=8, field_elem_size=256, max_K=50000)
    instance.plot_communication_cost()
    instance.plot_proof_size()