import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from categories.Category import Object,Operation, Morphism
from categories.Set import Set
from categories.TopologicalSpace import top
from categories.Group import grp
from categories.matrix import Matrix
from constants import sqrt, euclidean_distance

class SimplicalComplex(top):
    def __init__(self, vertices: list, simplices: list[list]):
        super().__init__(Set(vertices),simplices)
        if not self._verifySimplicies():
            raise ValueError("Does not match criteria for Simplical Complex")
    def _generate_combinations(self,arr, k):
        if k == 0:
            return [[]]
        if len(arr) < k:
            return []
        without_first = self._generate_combinations(arr[1:], k)
        with_first = self._generate_combinations(arr[1:], k - 1)
        for combo in with_first:
            combo.insert(0, arr[0])
        return with_first + without_first
    def _verifySimplicies(self):
        for simplex in self.topology:
            length = len(simplex)
            for k in range(1, length):  # Faces are subsets of length < len(simplex)
                faces = self._generate_combinations(simplex, k)
                for face in faces:
                    if face not in self.topology and sorted(face) not in self.topology:
                        print(f"Missing face {face} from simplex {simplex}")
                        return False
        return True
    def max_dimension(self):
        max_dim = -1
        for simplex in self.topology:
            dim = len(simplex) - 1
            if dim > max_dim:
                max_dim = dim
        return max_dim
    
    def get_simplices_of_dimension(self, k):
        result = []
        for simplex in self.topology:
            if len(simplex) - 1 == k:
                result.append(simplex)
        return result



class ChainGroup(grp):
    def __init__(self, simplices: list[list],coeffs:list):
        self.basis = [tuple(sorted(s)) for s in simplices]
        self.generator_labels = self.basis
        self.chains = self._generate_chains(coeffs=coeffs)
        chain_set = Set(self.chains)
        chain_op = Operation(self.chain_add)
        identity_chain = {b: 0 for b in self.generator_labels}
        super().__init__(chain_set, identity_chain, chain_op)
    def _generate_chains(self,coeffs:list):
        all_chains =[]
        self._build_chain(index=0,current={},all_chains=all_chains,coeffs=coeffs)
        return all_chains
    def _build_chain(self, index, current, all_chains:list, coeffs:list):
            if index == len(self.generator_labels):
                all_chains.append(current.copy())
                return
            for c in coeffs:
                current[self.generator_labels[index]] = c
                self._build_chain(index=index+1,current=current,all_chains=all_chains,coeffs=coeffs)
    def chain_add(self,chain1, chain2):
        result = {}
        for b in self.generator_labels:
            result[b] = chain1.get(b, 0) + chain2.get(b, 0)
        return result
    def create_chain(self, coeff_dict):
        chain = {}
        for b in self.generator_labels:
            chain[b] = coeff_dict.get(b, 0)
        return chain


class BoundaryOperation(Morphism):
    def __init__(self, domain_group: 'ChainGroup', codomain_group: 'ChainGroup'):
        self.domain = domain_group
        self.codomain = codomain_group
        self.map = {}
        for simplex in self.domain.generator_labels:
            self.map[simplex] = self._boundary(simplex)
    def _boundary(self, simplex: tuple):
            k = len(simplex)
            boundary = {}
            for i in range(k):
                face = simplex[:i] + simplex[i+1:]
                face = tuple(sorted(face))
                coeff = (-1) ** i
                if face in self.codomain.generator_labels:
                    boundary[face] = boundary.get(face, 0) + coeff
            return boundary
    def get_matrix(self):
        rows = len(self.codomain.generator_labels)
        cols = len(self.domain.generator_labels)
        matrix = []
        row_order = self.codomain.generator_labels
        col_order = self.domain.generator_labels
        for i in range(rows):
            row = []
            target_face = row_order[i]
            for j in range(cols):
                source_simplex = col_order[j]
                image_chain = self.map.get(source_simplex, {})
                row.append(image_chain.get(target_face, 0))
            matrix.append(row)
        return Matrix(matrix=matrix)
    

class Filtration:
    def __init__(self):
        self.levels = []  
    def add_complex(self, value, simplicial_complex):
        self.levels.append((value, simplicial_complex))
        self.levels.sort(key=lambda x: x[0])
    def get_filtration_levels(self):
        return [value for value, _ in self.levels]
    def get_complex_at(self, index):
        return self.levels[index][1]
    def get_all_complexes(self):
        return [sc for _, sc in self.levels]


class HomologyComputer:
    def __init__(self, simplicial_complex:SimplicalComplex):
        self.sc = simplicial_complex
        self.boundary_matrices = {}
        self.chain_groups = {}
        self.max_dim = self.sc.max_dimension()

    def compute_chain_groups(self):
        for k in range(self.max_dim + 1):
            simplices = self.sc.get_simplices_of_dimension(k)
            self.chain_groups[k] = ChainGroup(simplices)

    def compute_boundary_matrices(self):
        self.compute_chain_groups()
        for k in range(1, self.max_dim + 1):
            Ck = self.chain_groups[k]
            Ck_1 = self.chain_groups[k-1]
            boundary = BoundaryOperation(Ck, Ck_1)
            self.boundary_matrices[k] = boundary.get_matrix()

    def compute_betti_numbers(self):
        self.compute_boundary_matrices()
        betti_numbers = []
        for k in range(self.max_dim + 1):
            boundary_k = self.boundary_matrices.get(k, Matrix(0, 0, matrix=[]))
            boundary_kplus1 = self.boundary_matrices.get(k + 1, Matrix(0, 0, matrix=[]))

            null_k = boundary_k.nullity()
            rank_kplus1 = boundary_kplus1.rank()

            betti_k = null_k - rank_kplus1
            betti_numbers.append(betti_k)
        return betti_numbers



def build_vietoris_rips(points, epsilon, max_dim=2):
    simplicies =[]
    n = len(points)
    for i in range(n):
        simplicies.append([i])
    vertexes = simplicies.copy()
    for i in range(n):
        for j in range(i+1,n):
            if euclidean_distance(points[i], points[j]) <= epsilon:
                simplicies.append([i, j])
    if max_dim >= 2:
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if (euclidean_distance(points[i], points[j]) <= epsilon and
                        euclidean_distance(points[i], points[k]) <= epsilon and
                        euclidean_distance(points[j], points[k]) <= epsilon):
                        simplicies.append([i, j, k])
    return SimplicalComplex(vertices=vertexes, simplices=simplicies)

