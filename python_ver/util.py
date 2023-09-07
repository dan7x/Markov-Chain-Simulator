def tex_matrix(mat: list[any], vector=True):
    res = '$$\n\\begin{pmatrix}\n'
    if vector:
        mat = [str(x) for x in mat]
        res += ' \\\\\n'.join(mat) + '\n'
    else:
        mat = [[str(x) for x in y] for y in mat]
        res += ' \\\\\n'.join([' & '.join(x) for x in mat]) + '\n'
    res += '\\end{pmatrix}\n$$'
    return res

if __name__ == '__main__':
    print(tex_matrix([[1, 2, 3], [4, 5, 6]]))
