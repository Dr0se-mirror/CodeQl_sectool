// generated by codegen/codegen.py
private import codeql.swift.generated.Synth
private import codeql.swift.generated.Raw
import codeql.swift.elements.expr.Expr

class DotSyntaxBaseIgnoredExprBase extends Synth::TDotSyntaxBaseIgnoredExpr, Expr {
  override string getAPrimaryQlClass() { result = "DotSyntaxBaseIgnoredExpr" }

  Expr getImmediateQualifier() {
    result =
      Synth::convertExprFromRaw(Synth::convertDotSyntaxBaseIgnoredExprToRaw(this)
            .(Raw::DotSyntaxBaseIgnoredExpr)
            .getQualifier())
  }

  final Expr getQualifier() { result = getImmediateQualifier().resolve() }

  Expr getImmediateSubExpr() {
    result =
      Synth::convertExprFromRaw(Synth::convertDotSyntaxBaseIgnoredExprToRaw(this)
            .(Raw::DotSyntaxBaseIgnoredExpr)
            .getSubExpr())
  }

  final Expr getSubExpr() { result = getImmediateSubExpr().resolve() }
}