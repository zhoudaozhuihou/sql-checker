# SQL Analysis Prompt Template

## Response Structure
The analysis result should follow this JSON structure:
```json
{
    "safety_score": float,  // 0-100 score indicating query safety
    "performance_score": float,  // 0-100 score indicating query performance
    "issues": [
        {
            "type": "safety" | "performance",
            "severity": "high" | "medium" | "low",
            "description": string,
            "suggestion": string
        }
    ],
    "summary": string,  // Brief summary of the analysis
    "optimized_queries": {
        "safety_optimized": {
            "sql": string,  // SQL query with safety improvements
            "changes": [
                {
                    "type": string,  // Type of safety improvement
                    "description": string,  // Description of the change
                    "reason": string  // Reason for the change
                }
            ]
        },
        "performance_optimized": {
            "sql": string,  // SQL query with performance improvements
            "changes": [
                {
                    "type": string,  // Type of performance improvement
                    "description": string,  // Description of the change
                    "reason": string  // Reason for the change
                }
            ]
        },
        "combined_optimized": {
            "sql": string,  // SQL query with both safety and performance improvements
            "changes": [
                {
                    "type": string,  // Type of improvement
                    "category": "safety" | "performance",
                    "description": string,  // Description of the change
                    "reason": string  // Reason for the change
                }
            ]
        }
    }
}
```

## Common SQL Scenarios

### 1. Data Retrieval Queries
- Simple SELECT statements
- Complex JOIN operations
- Subqueries and CTEs
- Window functions
- Pagination queries

### 2. Data Modification Queries
- INSERT statements
- UPDATE operations
- DELETE operations
- MERGE/UPSERT operations
- Batch operations

### 3. Data Definition Queries
- CREATE TABLE
- ALTER TABLE
- DROP operations
- Index creation
- View definitions

### 4. Transaction Management
- BEGIN/COMMIT/ROLLBACK
- Savepoints
- Isolation levels
- Locking strategies

### 5. Stored Procedures and Functions
- Parameter handling
- Dynamic SQL
- Error handling
- Cursor usage

## Analysis Guidelines

### Safety Analysis
1. Check for SQL injection vulnerabilities
   - Look for direct string concatenation
   - Check for unescaped user input
   - Verify parameterized queries usage
   - Review dynamic SQL construction
   - Check for stored procedure injection

2. Verify proper parameter usage
   - Ensure all user inputs are parameterized
   - Check for proper type casting
   - Validate input ranges
   - Verify NULL handling
   - Check for proper escaping

3. Validate access control and permissions
   - Verify table access permissions
   - Check for excessive privileges
   - Review row-level security
   - Check for proper role usage
   - Verify schema ownership

4. Review sensitive data exposure
   - Identify sensitive data fields
   - Check for proper data masking
   - Review encryption usage
   - Check for proper logging
   - Verify audit trails

5. Check for potential data manipulation risks
   - Review UPDATE/DELETE operations
   - Check for proper WHERE clauses
   - Verify transaction boundaries
   - Check for proper locking
   - Review concurrency issues

### Performance Analysis
1. Evaluate query execution plan
   - Check for full table scans
   - Verify index usage
   - Analyze join operations
   - Review sort operations
   - Check for hash operations

2. Check for missing indexes
   - Identify frequently filtered columns
   - Check for composite index opportunities
   - Review index selectivity
   - Check for covering indexes
   - Verify index maintenance

3. Review table joins and subqueries
   - Optimize join order
   - Convert subqueries to joins when possible
   - Check for cartesian products
   - Review join types (INNER, LEFT, etc.)
   - Analyze join conditions

4. Analyze data volume impact
   - Check for large result sets
   - Review pagination implementation
   - Analyze data skew
   - Check for partition usage
   - Review data distribution

5. Check for potential bottlenecks
   - Identify N+1 query patterns
   - Check for redundant operations
   - Review locking contention
   - Analyze transaction duration
   - Check for resource usage

### Scoring Guidelines
- Safety Score:
  - 90-100: Very safe, follows best practices
    - All user inputs are properly parameterized
    - Proper access control implemented
    - Sensitive data properly handled
  - 70-89: Generally safe with minor concerns
    - Mostly parameterized queries
    - Basic access control in place
  - 50-69: Moderate safety concerns
    - Some unparameterized queries
    - Access control issues present
  - 0-49: Significant safety issues
    - Multiple SQL injection vulnerabilities
    - Critical access control problems

- Performance Score:
  - 90-100: Optimal performance
    - Proper indexes in place
    - Efficient join operations
    - Optimized query structure
  - 70-89: Good performance with minor optimizations possible
    - Most queries use indexes
    - Some room for join optimization
  - 50-69: Moderate performance concerns
    - Missing important indexes
    - Suboptimal join operations
  - 0-49: Significant performance issues
    - Multiple full table scans
    - Complex nested subqueries

### Issue Templates

#### Safety Issues
1. SQL Injection Risk
   - Description: "Query contains direct string concatenation with user input: [specific example]"
   - Suggestion: "Use parameterized queries with [specific database library] prepared statements"

2. Access Control Issue
   - Description: "Query accesses [table_name] without proper permission checks"
   - Suggestion: "Implement row-level security or add proper permission checks before query execution"

3. Sensitive Data Exposure
   - Description: "Query exposes sensitive data [specific fields] without proper masking"
   - Suggestion: "Implement data masking for [specific fields] or restrict access to authorized users only"

4. Transaction Safety
   - Description: "Transaction lacks proper error handling or rollback mechanism"
   - Suggestion: "Implement proper error handling with TRY-CATCH blocks and ensure proper rollback on failure"

5. Dynamic SQL Risk
   - Description: "Dynamic SQL construction using [specific method] may lead to injection"
   - Suggestion: "Use parameterized dynamic SQL with sp_executesql or equivalent"

6. Privilege Escalation
   - Description: "Query executed with elevated privileges [specific privilege]"
   - Suggestion: "Implement proper privilege separation and use least privilege principle"

#### Performance Issues
1. Missing Index
   - Description: "Column [column_name] in WHERE clause lacks proper index"
   - Suggestion: "Create index on [table_name]([column_name]) to improve query performance"

2. Inefficient Join
   - Description: "Join between [table1] and [table2] causes performance bottleneck"
   - Suggestion: "Optimize join by adding proper indexes or restructuring the query"

3. Large Result Set
   - Description: "Query returns [estimated_size] rows without pagination"
   - Suggestion: "Implement pagination with LIMIT and OFFSET clauses"

4. Transaction Performance
   - Description: "Transaction duration of [duration] exceeds recommended threshold"
   - Suggestion: "Break down transaction into smaller units or implement proper indexing"

5. Resource Contention
   - Description: "Query causes [specific type] lock contention on [table_name]"
   - Suggestion: "Implement proper isolation level or optimize locking strategy"

6. Data Skew
   - Description: "Uneven data distribution in [column_name] causing performance issues"
   - Suggestion: "Implement partitioning strategy or optimize query to handle skew"

### Scenario-Specific Analysis

#### 1. Pagination Queries
- Check for proper OFFSET/LIMIT usage
- Verify index coverage for pagination
- Review performance with large offsets
- Check for consistent ordering

#### 2. Batch Operations
- Verify proper batch size
- Check for transaction management
- Review error handling
- Analyze resource usage

#### 3. Reporting Queries
- Check for proper aggregation
- Verify index usage for grouping
- Review materialized view opportunities
- Analyze query complexity

#### 4. ETL Operations
- Verify proper error handling
- Check for data validation
- Review logging implementation
- Analyze performance bottlenecks

### Summary Template
The summary should follow this structure:
1. Overall assessment (safe/unsafe, performant/non-performant)
2. Key findings (2-3 most important issues)
3. Recommended actions (2-3 priority improvements)

Example: "Query is generally safe but has performance concerns. Key issues include missing index on user_id and inefficient join operation. Priority improvements: add index on user_id and optimize join between users and orders tables."

## Response Requirements
1. All scores must be between 0 and 100
2. Each issue must follow the provided templates
3. The summary must follow the three-part structure
4. Use specific technical details in descriptions
5. Provide concrete, implementable suggestions
6. Include specific table and column names in issues
7. Quantify performance impacts where possible
8. Reference specific code patterns in safety issues
9. Consider query context and usage patterns
10. Account for database-specific features and limitations
11. Include relevant statistics and metrics
12. Provide alternative solutions when applicable
13. Consider long-term maintenance implications
14. For each optimized query:
    - Clearly document all changes made
    - Explain the reasoning behind each change
    - Ensure changes maintain query functionality
    - Consider database-specific syntax
    - Preserve query semantics

15. Optimization Guidelines:
    - Safety optimizations should prioritize:
      - Parameterization of all user inputs
      - Proper escaping of special characters
      - Implementation of proper access controls
      - Addition of input validation
      - Proper error handling
    
    - Performance optimizations should prioritize:
      - Proper index usage
      - Efficient join operations
      - Optimal query structure
      - Appropriate data types
      - Resource-efficient operations

16. Combined Optimization Rules:
    - Safety improvements should not compromise performance
    - Performance improvements should not compromise safety
    - Changes should be clearly documented and explained
    - Original query functionality must be preserved
    - Changes should follow database best practices

### Optimization Examples

#### 1. Safety Optimization Example
Original Query:
```sql
SELECT * FROM users WHERE username = '$input'
```

Optimized Query:
```sql
SELECT * FROM users WHERE username = @username
```

Changes:
```json
{
    "type": "parameterization",
    "description": "Replaced direct string concatenation with parameter",
    "reason": "Prevent SQL injection by using parameterized queries"
}
```

#### 2. Performance Optimization Example
Original Query:
```sql
SELECT * FROM orders o 
JOIN customers c ON o.customer_id = c.id 
WHERE o.status = 'pending'
```

Optimized Query:
```sql
SELECT o.id, o.order_date, c.name, c.email 
FROM orders o 
JOIN customers c ON o.customer_id = c.id 
WHERE o.status = 'pending'
```

Changes:
```json
{
    "type": "column_selection",
    "description": "Specified required columns instead of using *",
    "reason": "Reduce data transfer and improve query performance"
}
```

#### 3. Combined Optimization Example
Original Query:
```sql
SELECT * FROM users WHERE username = '$input' AND status = 'active'
```

Optimized Query:
```sql
SELECT id, username, email, status 
FROM users 
WHERE username = @username 
AND status = 'active'
```

Changes:
```json
[
    {
        "type": "parameterization",
        "category": "safety",
        "description": "Replaced direct string concatenation with parameter",
        "reason": "Prevent SQL injection"
    },
    {
        "type": "column_selection",
        "category": "performance",
        "description": "Specified required columns",
        "reason": "Improve query performance"
    }
]
``` 