from common import *

# M = 1
# blowup_factor = 8
# l = 350
# N = 2**30
# T = N / M
# field_elem_size = 256
# num_bytes_per_elem = field_elem_size / 8

class Parallel_FRI:
    def __init__(self, circuit_size, num_of_queries, blowup_factor, field_elem_size):
        self.N = circuit_size
        self.l = num_of_queries
        self.blowup_factor = blowup_factor
        self.field_elem_size = field_elem_size
        self.num_bytes_per_elem = field_elem_size / 8

    def communication_cost_in_GB(self):
        print(f'Communication Cost: {0}GB')

    def proof_size_in_GB(self, M):
        T = self.N // M
        print("Proof size:")
        cost_1 = M  # Step 1: commitments of all local polynomials
        cost_2 = M * log(T)  # Step 2: FRI proof folding phase 
        cost_2 += M * self.l * 2 * log(T) * (1 + log(T))  # Step 2: FRI proof query phase
        total_cost = cost_1 + cost_2

        print(f'Step 1 costs {cost_1 / total_cost:.5f}')
        print(f'Step 2 costs {cost_2 / total_cost:.5f}')
        cost_in_GB = (total_cost * self.num_bytes_per_elem) / 10**9
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
    instance = Parallel_FRI(circuit_size=2**30, num_of_queries=350, blowup_factor=8, field_elem_size=256)
    instance.plot_proof_size()