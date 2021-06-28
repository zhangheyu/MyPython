# keep python && lua version consistent
import json

END = '{{END}}'  #{{}} not appear in user input
SUB_TREE = '{{SUB_TREE}}'
MATCH_ANY = '{{ANY}}'

PATH_MAX_DEPTH = 100 + 10  #presived 10 for host method protocol

# END = '$'
# SUB_TREE = '*'
# MATCH_ANY = '{}'

class PathWalker():
    def __init__(self, path):
        self.path = path

    def walk(self):
        start_idx = 0
        cur_idx = 1

        path = self.path
        # print('path:{}'.format(path))
        # print('path_len:{}'.format(len(path)))

        while cur_idx < len(path):
            # print('cur:', path[cur_idx])
            if path[cur_idx] != '/':
                cur_idx += 1
                continue
            # print(start_idx, cur_idx)
            assert(start_idx != cur_idx)
            
            yield path[start_idx: cur_idx]

            # print('after yild')
            start_idx = cur_idx
            cur_idx += 1

        yield path[start_idx:]

class PathMatcher():

    def __init__(self, path_dict):
        """
            注意，字典是引用，每次循环tree都会更新root，然后重新指向root继续遍历
        """
        root = {}

        for path, val in path_dict.items():
            print('path:', path)
            # print('value:', val)

            if not path:
                assert(False)

            tree = root
            if len(path.split('/')) > PATH_MAX_DEPTH:
                continue

            for segment in PathWalker(path).walk():
                print('segment:', segment)

                if segment.startswith('/{'):
                    segment = MATCH_ANY

                if segment.startswith('/*'):
                    segment = SUB_TREE

                if segment in tree:
                    print('in:', json.dumps(tree, indent=2))
                    tree = tree[segment]
                    print('tree[segment]:', json.dumps(tree, indent=2))
                else:
                    tree[segment] = {}
                    print('not in:', json.dumps(tree, indent=2))
                    tree = tree[segment]
            tree[END] = val
            print('root:', json.dumps(root, indent=2))

        self.root = root
        print('root:', self.root)

    def __str__(self):
        return json.dumps(self.root, indent=2)

    def match(self, path):

        if not path:
            return None

        path_segments = list(PathWalker(path).walk())

        ret = self.do_match_tree(self.root, path_segments)


        return ret.get(END) if ret else None

    def do_match_tree(self, tree, path_segments):

        if len(path_segments) == 0:
            return tree

        segment = path_segments[0]

        if segment in tree:
            ret = self.do_match_tree(tree[segment], path_segments[1:])
            if ret and END in ret:
                return ret

        if len(segment) > 1 and MATCH_ANY in tree:
            ret = self.do_match_tree(tree[MATCH_ANY], path_segments[1:])
            if ret and END in ret:
                return ret

        if SUB_TREE in tree:
            return tree[SUB_TREE]

        return None

def test_path_matcher():
    patterns = ["/", "/aa", "/aa/", "/bb/*", "/bb",
                "/cc/{id}/profile", "/cc/df/profile", "/cc/de/*", "/dd/{id}", "/dd/{id}/", "/ee/aa/bb/"]
    path_dict = {}
    for pattern in patterns:
        path_dict[pattern] = pattern
    print('path_dict', path_dict)

    matcher = PathMatcher(path_dict)
    print('matcher', matcher)


def test_path_match():
    assert(list(PathWalker("/cc/{id}/profile//").walk()) == ['/cc','/{id}', '/profile', '/', '/'])
    assert(list(PathWalker("/cc/{id}/profile/*").walk()) == ['/cc','/{id}', '/profile', '/*'])

    patterns = ["/", "/aa", "/aa/", "/bb/*", "/bb", "/cc/{id}/profile", "/cc/df/profile", "/cc/de/*", "/dd/{id}", "/dd/{id}/", "/ee/aa/bb/"]
    path_dict = {}
    for pattern in patterns:
        path_dict[pattern] = pattern
    print(path_dict)

    matcher = PathMatcher(path_dict)
    #print(matcher)

    assert(matcher.match('/') == '/')
    assert(matcher.match('/aa') == '/aa')
    assert(matcher.match('/aa/') == '/aa/')
    assert(matcher.match('/bb') == '/bb')
    assert(matcher.match('/bb/') == '/bb/*')
    assert(matcher.match('/bb/abac') == '/bb/*')
    assert(matcher.match('/bb/abac/fsd') == '/bb/*')
    assert(matcher.match('/cc/df/profile') == '/cc/df/profile')
    assert(matcher.match('/cc/123/profile') == '/cc/{id}/profile')
    assert(matcher.match('/cc/de/profile') == '/cc/de/*')
    assert(matcher.match('/dd/123') == '/dd/{id}')
    assert(matcher.match('/dd/123/') == '/dd/{id}/')

    matcher = PathMatcher({'10.10.65.21:80/GET/36/11/': 1,
                           '10.10.65.21:80/{}/36/11/': 2})

    assert(matcher.match('10.10.65.21:80/GET/36/11/') == 1)
    assert(matcher.match('10.10.65.21:80/POST/36/11/') == 2)


    matcher = PathMatcher({'10.10.65.21:80/GET/36/{}/': 1,
                           '10.10.65.21:80/{}/36/11/': 2})

    assert(matcher.match('10.10.65.21:80/GET/36/11/') == 1)
    assert(matcher.match('10.10.65.21:80/POST/36/11/') == 2)


    matcher = PathMatcher({'10.10.65.21:80/GET/36/{}/': 1,
                           '10.10.65.21:80/GET/{}/11/': 2})

    assert(matcher.match('10.10.65.21:80/GET/36/11/') == 1)
    assert(matcher.match('10.10.65.21:80/GET/38/11/') == 2)


    matcher = PathMatcher({'10.10.65.21:80/GET/*': 1,
                           '10.10.65.21:80/GET/{}/11/': 2})

    assert(matcher.match('10.10.65.21:80/GET/36/') == 1)
    assert(matcher.match('10.10.65.21:80/GET/36/11/') == 2)
    assert(matcher.match('10.10.65.21:80/GET/36/11') == 1)
    assert(matcher.match('10.10.65.21:80/GET/38/12/') == 1)



    matcher = PathMatcher({'10.10.65.21:80/GET/36/*': 1,
                           '10.10.65.21:80/GET/{}/11/': 2})

    assert(matcher.match('10.10.65.21:80/GET/36') == None)
    assert(matcher.match('10.10.65.21:80/GET/36/') == 1)
    assert(matcher.match('10.10.65.21:80/GET/36/11/') == 1)
    assert(matcher.match('10.10.65.21:80/GET/38/11/') == 2)
    assert(matcher.match('10.10.65.21:80/GET/38/11/aa') == None)
    assert(matcher.match('10.10.65.21:80/GET/38/11') == None)

    deep_path1 = '10.10.65.21:80/GET/' + '/'.join([str(i) for i in range(PATH_MAX_DEPTH - 10)])
    deep_path2 = '10.10.65.21:80/GET/' + '/'.join([str(i) for i in range(PATH_MAX_DEPTH)]) #ignore deep > PATH_MAX_DEPTH
    matcher = PathMatcher({deep_path1: 1, deep_path2:2})
    
    assert(matcher.match(deep_path1) == 1)
    assert(matcher.match(deep_path2) == None)

    matcher = PathMatcher({'10.10.65.21:80/GET/36/{id}': 1})
    
    assert(matcher.match('10.10.65.21:80/GET/36/') == None)
    assert(matcher.match('10.10.65.21:80/GET/36/3') == 1)
    assert(matcher.match('10.10.65.21:80/GET/36/3/') == None)
    
    matcher = PathMatcher({'10.10.65.21:80/GET/36/{id}': 1,
                           '10.10.65.21:80/GET/36/{id}/*': 2})
    
    assert(matcher.match('10.10.65.21:80/GET/36/') == None)
    assert(matcher.match('10.10.65.21:80/GET/36/3') == 1)
    assert(matcher.match('10.10.65.21:80/GET/36/3/') == 2)
    assert(matcher.match('10.10.65.21:80/GET/36/3/3') == 2)

if __name__ == '__main__':
    test_path_match()
    # test_path_matcher()
