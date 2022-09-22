# eye_tracking

#### Branch de referência para essa documentação é a branch dev

## Processo basicos realizados

### Estruturação da saida da atividade em um arquivo csv 

1. A saida dos outputs até agora consiste em uma dada estrutura padrão, por isso essa conversão de se torna facil.

#### Exemplo de dados:

0,0,,-2147483648,-2147483648,817,555,(NaN, NaN, NaN),(0.0, 0.0, 0.0, 1.0),Edu

1,15,2022_04_10 14_12_52.217,834,462,817,554,(NaN, NaN, NaN),(0.0, 0.0, 0.0, 1.0),Edu

* O primeiro 0 indica se foi detectado presença de olhar naquele momento ou não, 
normalmente até agora foi feito somente um filtro para considerar dados somente com o valor 1 nesse campo.

**0**   ,0,,-2147483648,-2147483648,817,555,(NaN, NaN, NaN),(0.0, 0.0, 0.0, 1.0),Edu

* O segundo é o frame de leitura, frame 1,2,3 etc.

1,**15**,2022_04_10 14_12_52.217,834,462,817,554,(NaN, NaN, NaN),(0.0, 0.0, 0.0, 1.0),Edu

* O terceiro é o momento no tempo em que o frame foi tirado, como é possivel ver. Se não foi detectado olha o momento retorna um valor negativo como por exemplo **-2147483648** .
Dessa forma realmente não faz sentido trabalhar com valores onde o olhar deu zero.

* Os proximos atributos são respectivamente **X,Y da tela**  **X,Y do mouse**. Os valores do mouse não são usados atualmente, só são mantido para possiveis utilizações.
Futuras

#### Processamento:

O processamento para pandas dataframe e posteriormente um csv serve para dividir melhor os dados. A manipulação de dados em geral é melhor com dataframes pandas.

Por exemplo a formação de colunas do dataframe atualmente segue esse padrão:
**CLASSE,INDICE,DATE_TIME,X_TELA,Y_TELA,X_MOUSE,Y_MOUSE,V1,V2,V3,V4,V5,V6,V7,NOME**

As colunas com o nome V1,V2 etc são dados que não estão sendo utilizados no momento

A manipulação se torna bem mais facil dessa forma. É possivel selecionar coluans especificas, contar os valores, realizar agrupamentos etc.

Essa estruturação no geral é feitas com as funções .replace()  e .split() do python para separar os campos.
Por exemplo:
.replace('(','') - Substitui onde têm a string '(' por ' '
.split(',') utiliza a string ',' para separar a linha em uma lista. Exemplo 'ad,cd,ef'.split(',') = ['ad','cd','ef']
