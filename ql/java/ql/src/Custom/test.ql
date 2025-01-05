/**
 * @name Test Query
 * @description This is a test query to demonstrate the use of @kind.
 * @kind problem
 * @problem.severity warning
 * @precision high
 * @id java/test-query
 */
import java

from MethodAccess printlnAccess
where
  printlnAccess.getMethod().hasName("println") and
  printlnAccess.getQualifier().toString() = "System.out"
select printlnAccess, "Avoid using System.out.println. Use a logger instead."