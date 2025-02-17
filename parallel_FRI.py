from common import *


class Parallel_FRI:
    def __init__(self, circuit_size, number_of_queries, blowup_factor, number_of_bits_per_field_elem):
        self.N = circuit_size
        self.l = number_of_queries
        self.blowup_factor = blowup_factor
        self.number_of_bytes_per_elem = number_of_bits_per_field_elem / NUMBER_OF_BITS_PER_BYTE


    def communication_cost_in_GB(self):
        print(f'Communication Cost: {0}GB')


    def proof_size_in_GB(self, M):
        T = self.N // M
        number_of_folding_rounds = log(T) - log(self.blowup_factor)

        cost_1 = M  # Step 1: commitments of all local polynomials
        cost_2 = M * number_of_folding_rounds  # Step 2: FRI proof folding phase 
        cost_3 = M * self.l * 2 * number_of_folding_rounds * (1 + log(T * self.blowup_factor))  # Step 3: FRI proof query phase
        total_cost = cost_1 + cost_2 + cost_3
        cost_in_GB = (total_cost * self.number_of_bytes_per_elem) / 10**9

        print("Proof size:")
        print(f'Step 1 costs {cost_1 / total_cost:.5f}')
        print(f'Step 2 costs {cost_2 / total_cost:.5f}')
        print(f'Step 3 costs {cost_3 / total_cost:.5f}')
        print(f'Proof size in GB: {cost_in_GB:.3f} GB')

        return cost_in_GB


    def plot_proof_size(self):
        fig = go.Figure()
        fig.update_layout(title="Proof Size for Parallel FRI", legend_title_text = "Proof size in GB")
        fig.update_xaxes(title_text="Number of Machines M")
        fig.update_yaxes(title_text="Proof Size in GB")

        x = []
        y = []
        for M in [2 ** i for i in range(9)]:
            x.append(M)
            y.append(self.proof_size_in_GB(M=M))

        fig.add_trace(go.Scatter(x=x, y=y, mode='markers+lines'))
        fig.show(config={'scrollZoom': True})



if __name__ == "__main__":
    # instance = Parallel_FRI(circuit_size=2**30, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256)
    # instance = Parallel_FRI(circuit_size=2**40, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256)
    instance = Parallel_FRI(circuit_size=2**50, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256)
    instance.plot_proof_size()