// generated by codegen/codegen.py
import codeql.swift.elements

/**
 * Gets any of the "immediate" children of `e`. "Immediate" means not taking into account node resolution: for example
 * if the AST child is the first of a series of conversions that would normally be hidden away, this will select the
 * next conversion down the hidden AST tree instead of the corresponding fully uncoverted node at the bottom.
 * Outside this module this file is mainly intended to be used to test uniqueness of parents.
 */
cached
Element getAnImmediateChild(Element e) {
  // why does this look more complicated than it should?
  // * none() simplifies generation, as we can append `or ...` without a special case for the first item
  none()
  or
  result = e.(Callable).getImmediateParam(_)
  or
  result = e.(Callable).getImmediateSelfParam()
  or
  result = e.(Callable).getImmediateBody()
  or
  result = e.(AbstractStorageDecl).getImmediateAccessorDecl(_)
  or
  result = e.(EnumCaseDecl).getImmediateElement(_)
  or
  result = e.(EnumElementDecl).getImmediateParam(_)
  or
  result = e.(IfConfigClause).getImmediateCondition()
  or
  result = e.(IfConfigClause).getImmediateElement(_)
  or
  result = e.(IfConfigDecl).getImmediateClause(_)
  or
  result = e.(PatternBindingDecl).getImmediateInit(_)
  or
  result = e.(PatternBindingDecl).getImmediatePattern(_)
  or
  result = e.(SubscriptDecl).getImmediateParam(_)
  or
  result = e.(TopLevelCodeDecl).getImmediateBody()
  or
  result = e.(AnyTryExpr).getImmediateSubExpr()
  or
  result = e.(ApplyExpr).getImmediateFunction()
  or
  result = e.(ApplyExpr).getImmediateArgument(_)
  or
  result = e.(Argument).getImmediateExpr()
  or
  result = e.(ArrayExpr).getImmediateElement(_)
  or
  result = e.(AssignExpr).getImmediateDest()
  or
  result = e.(AssignExpr).getImmediateSource()
  or
  result = e.(BindOptionalExpr).getImmediateSubExpr()
  or
  result = e.(CaptureListExpr).getImmediateBindingDecl(_)
  or
  result = e.(CaptureListExpr).getImmediateClosureBody()
  or
  result = e.(DictionaryExpr).getImmediateElement(_)
  or
  result = e.(DotSyntaxBaseIgnoredExpr).getImmediateQualifier()
  or
  result = e.(DotSyntaxBaseIgnoredExpr).getImmediateSubExpr()
  or
  result = e.(DynamicTypeExpr).getImmediateBase()
  or
  result = e.(EnumIsCaseExpr).getImmediateSubExpr()
  or
  result = e.(ExplicitCastExpr).getImmediateSubExpr()
  or
  result = e.(ForceValueExpr).getImmediateSubExpr()
  or
  result = e.(IdentityExpr).getImmediateSubExpr()
  or
  result = e.(IfExpr).getImmediateCondition()
  or
  result = e.(IfExpr).getImmediateThenExpr()
  or
  result = e.(IfExpr).getImmediateElseExpr()
  or
  result = e.(ImplicitConversionExpr).getImmediateSubExpr()
  or
  result = e.(InOutExpr).getImmediateSubExpr()
  or
  result = e.(InterpolatedStringLiteralExpr).getImmediateInterpolationCountExpr()
  or
  result = e.(InterpolatedStringLiteralExpr).getImmediateLiteralCapacityExpr()
  or
  result = e.(InterpolatedStringLiteralExpr).getImmediateAppendingExpr()
  or
  result = e.(KeyPathApplicationExpr).getImmediateBase()
  or
  result = e.(KeyPathApplicationExpr).getImmediateKeyPath()
  or
  result = e.(KeyPathExpr).getImmediateRoot()
  or
  result = e.(KeyPathExpr).getImmediateParsedPath()
  or
  result = e.(LazyInitializerExpr).getImmediateSubExpr()
  or
  result = e.(LookupExpr).getImmediateBase()
  or
  result = e.(MakeTemporarilyEscapableExpr).getImmediateEscapingClosure()
  or
  result = e.(MakeTemporarilyEscapableExpr).getImmediateNonescapingClosure()
  or
  result = e.(MakeTemporarilyEscapableExpr).getImmediateSubExpr()
  or
  result = e.(ObjCSelectorExpr).getImmediateSubExpr()
  or
  result = e.(OneWayExpr).getImmediateSubExpr()
  or
  result = e.(OpenExistentialExpr).getImmediateSubExpr()
  or
  result = e.(OpenExistentialExpr).getImmediateExistential()
  or
  result = e.(OpenExistentialExpr).getImmediateOpaqueExpr()
  or
  result = e.(OptionalEvaluationExpr).getImmediateSubExpr()
  or
  result = e.(RebindSelfInConstructorExpr).getImmediateSubExpr()
  or
  result = e.(RebindSelfInConstructorExpr).getImmediateSelf()
  or
  result = e.(SelfApplyExpr).getImmediateBase()
  or
  result = e.(SequenceExpr).getImmediateElement(_)
  or
  result = e.(SubscriptExpr).getImmediateArgument(_)
  or
  result = e.(TapExpr).getImmediateSubExpr()
  or
  result = e.(TapExpr).getImmediateBody()
  or
  result = e.(TupleElementExpr).getImmediateSubExpr()
  or
  result = e.(TupleExpr).getImmediateElement(_)
  or
  result = e.(TypeExpr).getImmediateTypeRepr()
  or
  result = e.(UnresolvedDotExpr).getImmediateBase()
  or
  result = e.(UnresolvedPatternExpr).getImmediateSubPattern()
  or
  result = e.(VarargExpansionExpr).getImmediateSubExpr()
  or
  result = e.(BindingPattern).getImmediateSubPattern()
  or
  result = e.(EnumElementPattern).getImmediateSubPattern()
  or
  result = e.(ExprPattern).getImmediateSubExpr()
  or
  result = e.(IsPattern).getImmediateCastTypeRepr()
  or
  result = e.(IsPattern).getImmediateSubPattern()
  or
  result = e.(OptionalSomePattern).getImmediateSubPattern()
  or
  result = e.(ParenPattern).getImmediateSubPattern()
  or
  result = e.(TuplePattern).getImmediateElement(_)
  or
  result = e.(TypedPattern).getImmediateSubPattern()
  or
  result = e.(TypedPattern).getImmediateTypeRepr()
  or
  result = e.(BraceStmt).getImmediateElement(_)
  or
  result = e.(CaseLabelItem).getImmediatePattern()
  or
  result = e.(CaseLabelItem).getImmediateGuard()
  or
  result = e.(CaseStmt).getImmediateBody()
  or
  result = e.(CaseStmt).getImmediateLabel(_)
  or
  result = e.(ConditionElement).getImmediateBoolean()
  or
  result = e.(ConditionElement).getImmediatePattern()
  or
  result = e.(ConditionElement).getImmediateInitializer()
  or
  result = e.(DeferStmt).getImmediateBody()
  or
  result = e.(DoCatchStmt).getImmediateBody()
  or
  result = e.(DoCatchStmt).getImmediateCatch(_)
  or
  result = e.(DoStmt).getImmediateBody()
  or
  result = e.(ForEachStmt).getImmediatePattern()
  or
  result = e.(ForEachStmt).getImmediateSequence()
  or
  result = e.(ForEachStmt).getImmediateWhere()
  or
  result = e.(ForEachStmt).getImmediateBody()
  or
  result = e.(GuardStmt).getImmediateBody()
  or
  result = e.(IfStmt).getImmediateThen()
  or
  result = e.(IfStmt).getImmediateElse()
  or
  result = e.(LabeledConditionalStmt).getImmediateCondition()
  or
  result = e.(RepeatWhileStmt).getImmediateCondition()
  or
  result = e.(RepeatWhileStmt).getImmediateBody()
  or
  result = e.(ReturnStmt).getImmediateResult()
  or
  result = e.(StmtCondition).getImmediateElement(_)
  or
  result = e.(SwitchStmt).getImmediateExpr()
  or
  result = e.(SwitchStmt).getImmediateCase(_)
  or
  result = e.(ThrowStmt).getImmediateSubExpr()
  or
  result = e.(WhileStmt).getImmediateBody()
  or
  result = e.(YieldStmt).getImmediateResult(_)
}

/**
 * Gets the "immediate" parent of `e`. "Immediate" means not taking into account node resolution: for example
 * if `e` has conversions, `getImmediateParent(e)` will give the bottom conversion in the hidden AST.
 */
Element getImmediateParent(Element e) {
  // `unique` is used here to tell the optimizer that there is in fact only one result
  // this is tested by the `library-tests/parent/no_double_parents.ql` test
  result = unique(Element x | e = getAnImmediateChild(x) | x)
}