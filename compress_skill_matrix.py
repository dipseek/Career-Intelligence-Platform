import joblib
from scipy.sparse import csr_matrix

# load current dense matrix
skill_matrix=joblib.load("models/skill_matrix.pkl")

print("original shape: ", skill_matrix.shape)
print("original type: ", type(skill_matrix))

# convert to sparse + smaller integer type
skill_matrix_sparse=csr_matrix(skill_matrix.astype("uint8"))

print("Sparse shape:", skill_matrix_sparse.shape)
print("Sparse type:", type(skill_matrix_sparse))

# Save compressed version
joblib.dump(
    skill_matrix_sparse,
    "models/skill_matrix_sparse.pkl"
)

print("Compressed skill matrix saved!")