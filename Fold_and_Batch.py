from common import *

class Fold_and_Batch:
    def __init__(self, circuit_size, number_of_queries, blowup_factor, number_of_bits_per_field_elem, max_K):
        self.N = circuit_size
        self.l = number_of_queries
        self.blowup_factor = blowup_factor
        self.number_of_bytes_per_field_elem = number_of_bits_per_field_elem / NUMBER_OF_BITS_PER_BYTE
        self.min_K = blowup_factor
        if max_K < blowup_factor:
            raise ValueError("max_K must be larger than the blowup factor!")
        self.max_K = max_K


    def communication_cost_in_GB(self, M, K):
        T = self.N // M
        number_of_local_folding_rounds = log(T) - log(K)

        cost_1 = M  # Step 1: Merkle commitments of all local polynomials
        cost_2 = M * number_of_local_folding_rounds  # Step 3: Merkle commitments of local intermediate folded polynomials
        cost_3 = M  # Step 4: sending random challenge to all worker nodes
        cost_4 = M * self.blowup_factor * K  # Step 5: workers sending partially folded local polynomials
        cost_5 = self.l * M + self.l * M * 2 * number_of_local_folding_rounds * (1 + log(T * self.blowup_factor))  # Step 8: folding checks for local folding
        total_cost = cost_1 + cost_2 + cost_3 + cost_4 + cost_5
        cost_in_GB = (total_cost * self.number_of_bytes_per_field_elem) / 10**9
        
        print(f'Step 1 costs {cost_1 / total_cost:.5f}')
        print(f'Step 3 costs {cost_2 / total_cost:.5f}')
        print(f'Step 4 costs {cost_3 / total_cost:.5f}')
        print(f'Step 5 costs {cost_4 / total_cost:.5f}')
        print(f'Step 8 costs {cost_5 / total_cost:.5f}')
        print(f'Total communication in GB: {cost_in_GB:.3f} GB')

        return cost_in_GB


    def proof_size_in_GB(self, M, K):
        T = self.N // M
        number_of_local_folding_rounds = log(T) - log(K)
        number_of_batched_folding_rounds = log(K) - log(self.blowup_factor)

        cost_1 = M  # Step 1: commitments of all local polynomials
        cost_2 = M * number_of_local_folding_rounds  # Step 3: Merkle commitments of locally folded polynomials  
        cost_3 = 1 + number_of_batched_folding_rounds  # Step 7: FRI proof folding phase for G(X)
        cost_4 = self.l * M * 2 * number_of_local_folding_rounds * (1 + log(T * self.blowup_factor))  # Step 8: folding checks for local folding
        cost_5 = self.l * 2 * number_of_batched_folding_rounds * (1 + log(K * self.blowup_factor))  # Step 9: folding checks for batched folding
        total_cost = cost_1 + cost_2 + cost_3 + cost_4 + cost_5
        cost_in_GB = (total_cost * self.number_of_bytes_per_field_elem) / 10**9

        print("Proof size:")
        print(f'Step 1 costs {cost_1 / total_cost:.5f}')
        print(f'Step 3 costs {cost_2 / total_cost:.5f}')
        print(f'Step 7 costs {cost_3 / total_cost:.5f}')
        print(f'Step 8 costs {cost_4 / total_cost:.5f}')
        print(f'Step 9 costs {cost_5 / total_cost:.5f}')
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
            # The method for computing comm. cost is only correct for K between blowup_factor * 2 and T/2
            for K in range(self.min_K * 2, min(T // 2, self.max_K), min(T // 2, self.max_K) // 20):
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
            # The method for computing cost is only correct for K up to T/2
            for K in range(self.min_K, min(T // 2, self.max_K), min(T // 2, self.max_K) // 20):
                x.append(K)
                y.append(self.proof_size_in_GB(M=M, K=K))
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers+lines', name=f'{M}'))
        
        fig.show(config={'scrollZoom': True})





if __name__ == "__main__":
    instance = Fold_and_Batch(circuit_size=2**35, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, max_K=100000)
    # instance = Fold_and_Batch(circuit_size=2**50, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, max_K=100000)
    # instance = Fold_and_Batch(circuit_size=2**30, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, max_K=10000)
    # instance = Fold_and_Batch(circuit_size=2**40, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, max_K=10**5)
    instance.plot_communication_cost()
    instance.plot_proof_size()