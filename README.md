# data-lineage-with-neo4j #
This project helps to see the data lineage.

## Implementation
With csv files as input nodes and relationships are created for columns and tables to improve the visualization.

## Data Model
![DataModel](https://github.com/iamhummingom/data-lineage-with-neo4j/blob/master/images/data_model.PNG)



## How to set up?
## Mac:
#### neo4j:

- Run neo4j container`docker run --rm --name neo4j -p 7474:7474 -p 7687:7687 -v $PWD/neo4j/data:/data -v $PWD/neo4j/import:/import neo4j`
- graph db will be available at - http://localhost:7474/
- Stop container: `docker stop neo4j`
- Remove image: `docker rmi neo4j`


#### loading data:

- Build image: `docker build --tag data_lineage -f Dockerfile .`
- Run container: `docker run --rm --name data_lineage  -v "$PWD":/data_lineage  --link neo4j --env-file ./env.list data_lineage`
- Remove image: `docker rmi data_lineage`
- env.list should be available in path with required environment variable values.

## Windows:

#### neo4j:
- Run neo4j container`docker run --rm --name neo4j -p 7474:7474 -p 7687:7687 -v %CD%/neo4j/data:/data -v %CD%/neo4j/import:/import neo4j`
- graph db will be available at - http://localhost:7474/
- Stop container: `docker stop neo4j`
- Remove image: `docker rmi neo4j`


#### loading data:

- Build image: `docker build --tag data_lineage -f Dockerfile .`
- Run container: `docker run --rm --name data_lineage  -v "%CD%":/data_lineage  --link neo4j --env-file ./env.list data_lineage`
- Remove image: `docker rmi data_lineage`
- env.list should be available in path with required environment variable values.

#### Environment variables
| Variable | Description            |   Default  | Required 
|----------|------------------------|:----------:|:--------:
| `RECREATE_SCHEMA` | To receate the schema. Allowed value : [True/False]  |    False       |    no   | 
| `TRIGGER_STATUS`| neo4j password - first time its neo4j, after that it needs tobe changed as saved in variable            |    -       |    yes   |

## Sample questions to ask from your data
#### Show me all column descriptions
```
match (c:Column)-[:BELONGS_TO]-(table:Table{name: 'final_table'})
where c.description is not null
return table.name, c.name,c.description
```
#### Show me a column (table to table transfer example)
```
match (c:Column)
where c.name='first_name'
return c
```
#### Show me a column (which is derived from multiple columns example)
```
match (c:Column)
where c.name='full_name'
return c
```
#### Show me how one column populates (here only 2 traverse are chosen)
```
match (target:Column{name:'full_name'})
<-[rel:CREATES*1..2]-(source)-[p:BELONGS_TO]->(table:Table)
return target,rel,source
limit 100
```
#### Show me the columns which is not used
```
match (source:Column)-[:BELONGS_TO]->(table:Table)
where NOT (source)-[:CREATES]->()
AND NOT(source)-[:BELONGS_TO]->(:Table{name:'final_table'})
return source.name,table.name
limit 100
```
#### Show me source to target column path
```
match (target:Column{name:'full_name'})
match (source:Table)
match path= shortestPath((source)-[*..3]-(target))
return path
```