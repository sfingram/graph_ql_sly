# GraphQL SLY

A GraphQL parser built using the SLY library.

## example

```python
import graph_ql_sly.parser as gqp
gqp.parse_string("""{
  human(id: "1000") {
    name
    height(unit: "FOOT")
  }
}""")
```

```
ExecutableDefinition(
  OperationDefinition(
    operation_type='query',
    name=None,
    selection_set=SelectionSet(
      Selection(
        Field(
          name='human',
          arguments=Arguments(
            Argument(
              name=id,
              value="1000"
            )
          ),
          selection_set=SelectionSet(
            Selection(
              Field(
                name='name',
                arguments=None,
                selection_set=None
              )
            ),
            Selection(
              Field(
                name='height',
                arguments=Arguments(
                  Argument(
                    name=unit,
                    value="FOOT"
                  )
                ),
                selection_set=None
              )
            )
          )
        )
      )
    )
  )
)
```
