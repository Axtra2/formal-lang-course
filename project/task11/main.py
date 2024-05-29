from antlr4.InputStream import *
from antlr4 import *

from project.task11.gggg.project.task11.ggggListener import ggggListener
from project.task11.gggg.project.task11.ggggVisitor import ggggVisitor
from project.task11.gggg.project.task11.ggggParser import ggggParser
from project.task11.gggg.project.task11.ggggLexer import ggggLexer


def prog_to_tree(program: str) -> tuple[ParserRuleContext, bool]:
    lexer = ggggLexer(InputStream(program))
    parser = ggggParser(CommonTokenStream(lexer))
    return (parser.prog(), parser.getNumberOfSyntaxErrors() == 0)


def nodes_count(tree: ParserRuleContext) -> int:
    class NodeCounter(ggggListener):
        def __init__(self) -> None:
            super(ggggListener, self).__init__()
            self.nodeCount = 0

        def enterEveryRule(self, ctx):
            self.nodeCount += 1

    counter = NodeCounter()
    tree.enterRule(counter)
    return counter.nodeCount


def tree_to_prog(tree: ParserRuleContext) -> str:
    class TextListener(ggggListener):
        def __init__(self):
            super(ggggListener, self).__init__()
            self.text = ""

        def enterEveryRule(self, rule):
            self.text += rule.getText()

    tl = TextListener()
    tree.enterRule(tl)
    return tl.text
