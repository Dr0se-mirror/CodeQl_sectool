// generated by codegen/codegen.py
private import codeql.swift.generated.Synth
private import codeql.swift.generated.Raw
import codeql.swift.elements.expr.DynamicLookupExpr

class DynamicMemberRefExprBase extends Synth::TDynamicMemberRefExpr, DynamicLookupExpr {
  override string getAPrimaryQlClass() { result = "DynamicMemberRefExpr" }
}