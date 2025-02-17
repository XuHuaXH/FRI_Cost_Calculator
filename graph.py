from parallel_FRI import *
from Fold_and_Batch import *
from Distributed_Batched_FRI import *

if __name__ == "__main__":

    # N = 2^30
    parallel_FRI_instance = Parallel_FRI(circuit_size=2**30, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256)
    fold_and_batch_instance = Fold_and_Batch(circuit_size=2**30, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, max_K=10000)
    distributed_batched_FRI_instance = Distributed_Batched_FRI(circuit_size=2**30, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, min_S=15, max_S=50)

    # # N = 2^40
    # parallel_FRI_instance = Parallel_FRI(circuit_size=2**40, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256)
    # fold_and_batch_instance = Fold_and_Batch(circuit_size=2**40, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, max_K=10**5)
    # distributed_batched_FRI_instance = Distributed_Batched_FRI(circuit_size=2**40, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, min_S=40, max_S=300)
    
    # # N = 2^50
    # parallel_FRI_instance = Parallel_FRI(circuit_size=2**50, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256)
    # fold_and_batch_instance = Fold_and_Batch(circuit_size=2**50, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, max_K=100000)
    # distributed_batched_FRI_instance = Distributed_Batched_FRI(circuit_size=2**50, number_of_queries=50, blowup_factor=8, number_of_bits_per_field_elem=256, min_S=50, max_S=400)

    parallel_FRI_instance.plot_proof_size()
    fold_and_batch_instance.plot_communication_cost()
    fold_and_batch_instance.plot_proof_size()
    distributed_batched_FRI_instance.plot_communication_cost()
    distributed_batched_FRI_instance.plot_proof_size()