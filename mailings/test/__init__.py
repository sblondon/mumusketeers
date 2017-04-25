import markdownmail


class AbstractMailServer(markdownmail.NullServer):
    def check(self, markdownmail):
        assert markdownmail._parts[0]
        assert markdownmail._parts[1]

