def keyGet(clef,nsharps,nflats):
    if clef == 'treble' or 'Treble':
        trebCKey = [1, 3, 4, 6, 8, 10, 11, 13, 15, 16, 18]
        trebSharpChanges = {
            7: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            6: [0, 1, 2, 3, 4, 6, 7, 8, 9, 10],
            5: [0, 2, 3, 4, 6, 7, 9, 10],
            4: [0, 2, 3, 6, 7, 9, 10],
            3: [2, 3, 6, 9, 10],
            2: [2, 6, 9],
            1: [2, 9]}
        trebFlatChanges = {
            7: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            6: [0, 1, 3, 4, 5, 6, 7, 8, 10],
            5: [0, 1, 3, 4, 5, 7, 8, 10],
            4: [0, 1, 4, 5, 7, 8],
            3: [1, 4, 5, 8],
            2: [1, 5, 8],
            1: [5]
        }
        key = trebCKey
        if nsharps != 0:
            changes = trebSharpChanges[nsharps]
            for idx in changes:
                key[idx] += 1
            return key
        elif nflats != 0:
            changes = trebFlatChanges[nflats]
            for idx in changes:
                key[idx] -= 1
            return key
        else:
            return key
    elif clef == 'bass' or 'Bass':
        bassCKey = [1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19]
        bassSharpChanges = {
            7: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            6: [0, 1, 2, 4, 5, 6, 7, 8, 9],
            5: [0, 1, 2, 4, 5, 7, 8, 9],
            4: [0, 1, 4, 5, 7, 8],
            3: [0, 1, 4, 7, 8],
            2: [0, 4, 7],
            1: [0, 7]
        }
        bassFlatChanges = {
            7: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            6: [1, 2, 3, 4, 5, 6, 8, 9, 10],
            5: [1, 2, 3, 5, 6, 8, 9, 10],
            4: [2, 3, 5, 6, 9, 10],
            3: [2, 3, 6, 9, 10],
            2: [3, 6, 10],
            1: [3, 6]
        }
        key = bassCKey
        if nsharps != 0:
            changes = bassSharpChanges[nsharps]
            for idx in changes:
                key[idx] += 1
            return key
        elif nflats != 0:
            changes = bassFlatChanges[nflats]
            for idx in changes:
                key[idx] -= 1
            return key
        else:
            return key
