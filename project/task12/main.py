from project.task12.gggg.ggggVisitor import *
from project.task12.gggg.ggggParser import *
from project.task12.gggg.ggggLexer import *

from typing import *
import traceback
import copy


class Typer(ggggVisitor):
    def __init__(self):
        self.context = {}

    # Visit a parse tree produced by ggggParser#prog.
    def visitProg(self, ctx: ggggParser.ProgContext):
        print("prog")
        self.visitChildren(ctx)
        return None

    # Visit a parse tree produced by ggggParser#stmt.
    def visitStmt(self, ctx: ggggParser.StmtContext):
        print("stmt")
        self.visitChildren(ctx)
        return None

    # Visit a parse tree produced by ggggParser#declare.
    def visitDeclare(self, ctx: ggggParser.DeclareContext):
        print("declare")
        self.context[ctx.VAR().getText()] = "graph"
        return None

    # Visit a parse tree produced by ggggParser#bind.
    def visitBind(self, ctx: ggggParser.BindContext):
        print("bind")
        self.context[ctx.VAR().getText()] = self.visitExpr(ctx.expr())
        return None

    # Visit a parse tree produced by ggggParser#remove.
    def visitRemove(self, ctx: ggggParser.RemoveContext):
        print("remove")
        var = ctx.VAR().getText()
        if var in self.context:
            if self.context[var] != "graph":
                raise Exception("Attemt to remove not from graph")
        else:
            raise Exception("Use of undeclared variable " + var)
        a = self.visitExpr(ctx.expr())
        t = ctx.getChild(1).getText()
        if t == "vertex":
            if a != "int":
                raise Exception("Type error in remove")
            else:
                pass
        elif t == "edge":
            if a != "int*int*int":
                raise Exception("Type error in remove")
        elif t == "vertices":
            if a != "set<int>":
                raise Exception("Type error in remove")
        return None

    # Visit a parse tree produced by ggggParser#add.
    def visitAdd(self, ctx: ggggParser.AddContext):
        print("add")
        var = ctx.VAR().getText()
        if var in self.context:
            if self.context[var] != "graph":
                raise Exception("Attemt to add not to graph")
        else:
            raise Exception("Use of undeclared variable " + var)
        self.visitExpr(ctx.expr())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ggggParser#expr.
    def visitExpr(self, ctx: ggggParser.ExprContext):
        print("add")
        if ctx.NUM():
            return "int"
        elif ctx.CHAR():
            return "char"
        elif ctx.VAR():
            var = ctx.VAR().getText()
            if var not in self.context:
                self.context[var] = "FA"
            return self.context[var]
        elif ctx.edge_expr():
            return self.visitEdge_expr(ctx.edge_expr())
        elif ctx.set_expr():
            return self.visitSet_expr(ctx.set_expr())
        elif ctx.regexp():
            return self.visitRegexp(ctx.regexp())
        elif ctx.select():
            return self.visitSelect(ctx.select())
        else:
            raise Exception("Unknown expression type")

    # Visit a parse tree produced by ggggParser#set_expr.
    def visitSet_expr(self, ctx: ggggParser.Set_exprContext):
        elem_types = [self.visitExpr(expr) for expr in ctx.expr()]
        if all(t == "int" for t in elem_types):
            return "set<int>"
        raise Exception("Bad set elements")

    # Visit a parse tree produced by ggggParser#edge_expr.
    def visitEdge_expr(self, ctx: ggggParser.Edge_exprContext):
        return "int*int*int"

    # Visit a parse tree produced by ggggParser#regexp.
    def visitRegexp(self, ctx: ggggParser.RegexpContext):
        if ctx.CHAR():
            return "FA"
        elif ctx.VAR():
            var = ctx.VAR().getText()
            if var in self.context:
                return self.context[var]
            return "RSM"
        elif len(ctx.regexp()) == 1:
            return self.visitRegexp(ctx.regexp()[0])

        a = ctx.regexp()[0]
        b = ctx.regexp()[1]

        x = 0
        if self.visitRegexp(a) == "RSM":
            x += 1
        if self.visitRegexp(b) == "RSM":
            x += 1
        print(x, a.getText(), b.getText())

        if x == 0:
            return "FA"
        elif x == 2 and ctx.getChild(1).getText() == "&":
            raise Exception("Attempt to intersect RSMs")
        else:
            return "RSM"

    # Visit a parse tree produced by ggggParser#range.
    def visitRange(self, ctx: ggggParser.RangeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ggggParser#select.
    def visitSelect(self, ctx: ggggParser.SelectContext):
        initContext = copy.deepcopy(self.context)
        for vf in ctx.v_filter():
            self.visitV_filter(vf)
        t = self.visitExpr(ctx.expr())
        if t != "FA" and t != "RSM":
            raise Exception("Wrong constraint type")
        if len(ctx.VAR()) == 4:
            return "set<int>"
        else:
            return "set<int*int>"
        self.context = initContext

    # Visit a parse tree produced by ggggParser#v_filter.
    def visitV_filter(self, ctx: ggggParser.V_filterContext):
        var = ctx.VAR().getText()
        if var in self.context:
            raise Exception("Redefinition of " + var)
        t = self.visitExpr(ctx.expr())
        t = t.split("<")
        if len(t) != 2:
            raise Exception("Type error in filter")
        t = t[1].split(">")
        if len(t) != 2:
            raise Exception("Type error in filter")
        t = t[0]
        if t != "int":
            raise Exception("Type error in filter")
        self.context[var] = t
        return None


def typing_program(program: str) -> bool:
    lexer = ggggLexer(InputStream(program))
    parser = ggggParser(CommonTokenStream(lexer))
    if parser.getNumberOfSyntaxErrors() != 0:
        print("Incorrect syntax")
        return False

    tree = parser.prog()
    typer = Typer()
    try:
        typer.visit(tree)
        print(typer.context)
        return True
    except:
        print(typer.context)
        print(traceback.format_exc())
        return False


def exec_program(program: str) -> dict[str, set[tuple]]:
    pass
