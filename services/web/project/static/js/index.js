
console.log('url_resemploigraph indexjs',url_resemploigraph)


const colorLegend = (selection, props) => {
  const {
    colorScale,
    circleRadius,
    spacing,
    textOffset
  } = props;

  const groups = selection.selectAll('g')
    .data(colorScale.domain());
  const groupsEnter = groups
    .enter().append('g')
      .attr('class', 'tick');
  groupsEnter
    .merge(groups)
      .attr('transform', (d, i) =>
        `translate(0, ${i * spacing})`
      );
  groups.exit().remove();

  groupsEnter.append('circle')
    .merge(groups.select('circle'))
      .attr('r', circleRadius)
      .attr('fill', colorScale);

  groupsEnter.append('text')
    .merge(groups.select('text'))
      .text(d => d)
      .attr('dy', '0.32em')
      .attr('x', textOffset);
}

function tabulate(html_element,data, columns, title) {
  var table = d3.select(html_element).append("table"),
      thead = table.append("thead"),
      tbody = table.append("tbody");

  // Append the header row
  thead.append("tr")
      .selectAll("th")
      .data(columns)
      .enter()
      .append("th")
          .text(function(column) {
              return column;
          });

  // Create a row for each object in the data
  var rows = tbody.selectAll("tr")
      .data(data)
      .enter()
      .append("tr");

  // Create a cell in each row for each column
  var cells = rows.selectAll("td")
      .data(function(row) {
          return columns.map(function(column) {
              return {
                  column: column,
                  value: row[column]
              };
          });
      })
      .enter()
      .append("td")
          .text(function(d) { return d.value; });

  return table;}

const barChart= (data,svg2, margin, xValue, yValuecumul_depuis_jan_recrutements_externes, title, objectif, show_objectif=true) => {

  const xAxisTickFormat = date => date.toLocaleDateString('fr-FR', {month: 'short', year :"2-digit"})

  
  const width = +svg2.attr('width');
  const height = +svg2.attr('height');
  
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const xScalebar = d3.scaleBand()
          .domain(data.map(xValue))
          .range([0,innerWidth])
          .paddingInner(0.15);  
  
  const yScalebar = d3.scaleLinear()
    .domain([0,Math.max(d3.max(data, yValuecumul_depuis_jan_recrutements_externes),objectif)])
    .range([innerHeight,0])
    .nice();  

  const xAxisbar = d3.axisBottom(xScalebar)                      
                      .tickFormat(xAxisTickFormat);

  const g2 = svg2.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);


  const chart = g2;

    chart.append('g')
      .call(d3.axisLeft(yScalebar).tickSize(-innerWidth))
      .selectAll('.domain')
      .remove();


    chart.append('g')
      .call(xAxisbar)
      .attr('transform', `translate(${0},${innerHeight})`)
      .selectAll('.domain, .tick line')
      .remove();
     
  //add line
  console.log('xscale',xScalebar(+0))
  console.log(yScalebar(objectif))

  

  const barGroups = chart.selectAll()
      .data(data)
      .enter()
      .append('g')
   
       barGroups
         .append('rect')
         .attr('fill', '#FF7900')
         .attr('class', 'bar')
         .attr('x', (d) => xScalebar(xValue(d)))
         .attr('y', (d) => yScalebar(yValuecumul_depuis_jan_recrutements_externes(d)))
         .attr('height', (d) => innerHeight - yScalebar(yValuecumul_depuis_jan_recrutements_externes(d)))
         .attr('width', xScalebar.bandwidth())
         .on('mouseenter', function (actual, i) {
           d3.selectAll('.value')
             .attr('opacity', 0)
   
           d3.select(this)
             .transition()
             .duration(300)
             .attr('opacity', 0.6)
             .attr('x', (d) => xScalebar(xValue(d)) - 5)
             .attr('width', xScalebar.bandwidth() + 10)
   
           const y = yScalebar(yValuecumul_depuis_jan_recrutements_externes(actual))
   
           line = chart.append('line')
             .attr('id', 'limit')
             .attr('x1', 0)
             .attr('y1', y)
             .attr('x2', width)
             .attr('y2', y)
   
           barGroups.append('text')
             .attr('class', 'divergence')
             .attr('x', (d) => xScalebar(xValue(d)) + xScalebar.bandwidth() / 2)
             .attr('y', (d) => yScalebar(yValuecumul_depuis_jan_recrutements_externes(d)) - 5)
             .attr('fill', 'black')
             .attr('text-anchor', 'middle')
             .text((d, idx) => {
               console.log(idx,'idx')
               //en commentaire, ce qui permet d'avoir la diff entre les colonnes
               //const divergence = (yValuecumul_depuis_jan_recrutements_externes(d) - yValuecumul_depuis_jan_recrutements_externes(actual)).toFixed(1)
               const divergence = (yValuecumul_depuis_jan_recrutements_externes(d) - objectif).toFixed(1)
               let text = ''
               if (divergence > 0) text += '+'
               text += `${divergence}`

               console.log(text,'text')

               //return idx !== i ? text : '';
               return idx !== i ? '' : text ;
             })
   
         })
         .on('mouseleave', function () {
           d3.selectAll('.value')
             .attr('opacity', 1)
   
           d3.select(this)
             .transition()
             .duration(300)
             .attr('opacity', 1)
             .attr('x', (d) => xScalebar(xValue(d)))
             .attr('width', xScalebar.bandwidth())
   
           chart.selectAll('#limit').remove()
           chart.selectAll('.divergence').remove()
         })
   
    barGroups 
      .append('text')
      .attr('class', 'value')
      .attr('x', (d) => xScalebar(xValue(d)) + xScalebar.bandwidth() / 2)
      .attr('y', (d) => yScalebar(yValuecumul_depuis_jan_recrutements_externes(d)) - 5)
      .attr('text-anchor', 'middle')
      .text((d) => `${yValuecumul_depuis_jan_recrutements_externes(d)}`)

    
    if(show_objectif===true){

      //add objectif to title
      chart.append('text')
         .attr('class', 'title')
         .attr('y', -10)
         .text(title + ' (objectif: ' + objectif+ ')');

      //add objectif line
      chart.append("line")
        .style("stroke","black")
        .style("stroke-width", 2)
        .attr("x1",0)
        .attr("y1",yScalebar(objectif))
        .attr("x2",innerWidth)
        .attr("y2",yScalebar(objectif));
    }
    else{
      chart.append('text')
        .attr('class', 'title')
        .attr('y', -10)
        .text(title);
    }
}

const groupedBarchart = (data,svg,margin, xValue, title) => {

  let objectif=0

  const xAxisTickFormat = date => date.toLocaleDateString('fr-FR', {month: 'short', year :"2-digit"})
  let yValuecumul_depuis_jan_recrutements_externes = d => d.mobilites_entrantes
  let yValue_mob_sortantes = d => d.mobilites_sortantes
  
  const width = +svg.attr('width');
  const height = +svg.attr('height');
  
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const xScalebar = d3.scaleBand()
          .domain(data.map(xValue))
          .range([0,innerWidth])
          .paddingInner(0.15);  
  
  const yScalebar = d3.scaleLinear()
    .domain([0,Math.max(d3.max(data, yValuecumul_depuis_jan_recrutements_externes),d3.max(data, yValue_mob_sortantes))])
    .range([innerHeight,0])
    .nice();  

  const xAxisbar = d3.axisBottom(xScalebar)                      
                      .tickFormat(xAxisTickFormat);

  const g2 = svg.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  const chart = g2;

    chart.append('g')
      .call(d3.axisLeft(yScalebar).tickSize(-innerWidth))
      .selectAll('.domain')
      .remove();


    chart.append('g')
      .call(xAxisbar)
      .attr('transform', `translate(${0},${innerHeight})`)
      .selectAll('.domain, .tick line')
      .remove();

  const barGroups = chart.selectAll()
      .data(data)
      .enter()
      .append('g')
   
      barGroups
         .append('rect')
         .attr('fill', '#FF7900')
         .attr('class', 'bar')
         .attr('x', (d) => xScalebar(xValue(d)))
         .attr('y', (d) => yScalebar(yValuecumul_depuis_jan_recrutements_externes(d)))
         .attr('height', (d) => innerHeight - yScalebar(yValuecumul_depuis_jan_recrutements_externes(d)))
         .attr('width', xScalebar.bandwidth()/2)
      
      barGroups
         .append('rect')
         .attr('fill', '#9164CD')
         .attr('class', 'bar')
         .attr('x', (d) => xScalebar(xValue(d)) + xScalebar.bandwidth()/2)
         .attr('y', (d) => yScalebar(yValue_mob_sortantes(d)))
         .attr('height', (d) => innerHeight - yScalebar(yValue_mob_sortantes(d)))
         .attr('width', xScalebar.bandwidth()/2)
   
    barGroups 
      .append('text')
      .attr('class', 'value')
      .attr('x', (d) => xScalebar(xValue(d)) + xScalebar.bandwidth() / 2)
      .attr('y', (d) => yScalebar(yValuecumul_depuis_jan_recrutements_externes(d)) - 5)
      .attr('text-anchor', 'middle')
      .text((d) => `${yValuecumul_depuis_jan_recrutements_externes(d)-yValue_mob_sortantes(d)}`)

    chart.append('text')
      .attr('class', 'title')
      .attr('y', -10)
      .text(title);

}

const stackedbarchart = (data,svg) => {
  
  let margin = {top: 20, right: 100, bottom: 200, left: 40},
      width = +svg.attr("width") - margin.left - margin.right,
      height = +svg.attr("height") - margin.top - margin.bottom;

      
  var keys =["alt percent","cdd percent","cdi percent"]

  // set x scale
  var x = d3.scaleBand()
      .rangeRound([0, width])
      .paddingInner(0.05)
      .domain(data.map(function(d) { return d['nom um']; }))
      .align(0.1);

  // set y scale
  var y = d3.scaleLinear()
        .domain([0, 100])
        .nice()
        .rangeRound([height, 0]);

  // set the colors
  var z = d3.scaleOrdinal()
    .domain(keys)
    .range(["#4bb4e6", "#ff7900", 	"#9164CD"]); //"#50be87" vert-bleu


  //var keys = data.columns.slice(1);

  //data.sort(function(a, b) { return b.total - a.total; });

  g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  g.append("g")
    .selectAll("g")
    .data(d3.stack().keys(keys)(data))
    .enter().append("g")
      .attr("fill", function(d) { return console.log(z(d.key)),z(d.key); })
    .selectAll("rect")
    .data(function(d) { return d; })
    .enter().append("rect")
      .attr("x", function(d) { return x(d.data['nom um']); })
      .attr("y", function(d) { return y(d[1]); }) 
      .attr("height", function(d) { return y(d[0]) - y(d[1]); })
      .attr("width", x.bandwidth())
    .on("mouseover", function() { tooltip.style("display", null); })
    .on("mouseout", function() { tooltip.style("display", "none"); })
    .on("mousemove", function(d) {
      var xPosition = d3.mouse(this)[0] - 5;
      var yPosition = d3.mouse(this)[1] - 5;
      tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
      tooltip.select("text").text(d[1]-d[0]);
    });

  g.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
      .selectAll("text")	
        .style("text-anchor", "end")
        .style("font-size","0.6rem")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)");

  g.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(y).ticks(null, "s"))
    .append("text")
      .attr("x", 2)
      .attr("y", y(y.ticks().pop()) + 0.5)
      .attr("dy", "0.32em")
      .attr("fill", "#000")
      .attr("font-weight", "bold")
      .attr("text-anchor", "start");

  var legend = g.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("text-anchor", "end")
    .selectAll("g")
    .data(keys.slice().reverse())
    .enter().append("g")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
      .attr("x", width - 19)
      .attr("width", 19)
      .attr("height", 19)
      .attr("fill", z);

  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9.5)
      .attr("dy", "0.32em")
      .text(function(d) { return d; });

  // Prep the tooltip bits, initial display is hidden
  var tooltip = svg.append("g")
    .attr("class", "tooltip")
    .style("display", "none");
      
  tooltip.append("rect")
    .attr("width", 60)
    .attr("height", 20)
    .attr("fill", "white")
    .style("opacity", 0.5);

  tooltip.append("text")
    .attr("x", 30)
    .attr("dy", "1.2em")
    .style("text-anchor", "middle")
    .attr("font-size", "12px")
    .attr("font-weight", "bold");
}

const svg = d3.select('#svg1');

const width = +svg.attr('width');
const height = +svg.attr('height');



const render = data => {
  
    const title = 'Nombre de CDI';

    const xValue = d => d.date

    const yValue = d => d.nb_cdi_actifs
    const yValueetpcdi = d => d.ETP_cdiactifs
    const yValueetpbudget = d => d.ETP_budgetHRZ_cdiactifs 


    const circleRadius = 6;
    const xAxisLabel = 'Mois';
    const yAxisLabel = 'Effectif';


    
    const margin = { top: 60, right: 200, bottom: 88, left: 105 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;
    
    const xScale = d3.scaleTime()
      .domain(d3.extent(data, xValue))
      .range([0, innerWidth])
      .nice();

    console.log('xscale', xScale)

    const yScale = d3.scaleLinear()
      .domain([8000, d3.max(data, yValue)])
      .range([innerHeight, 0])
      .nice();
    
    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    
    
    const xAxisTickFormat = date => date.toLocaleDateString('fr-FR', {month: 'short', year :"2-digit"})

    const xAxis = d3.axisBottom(xScale)
      .tickSize(-innerHeight)
      .tickFormat(xAxisTickFormat)
      .tickPadding(15);
    
    //console.log(xScale(data))

    const yAxis = d3.axisLeft(yScale)
      .tickSize(-innerWidth)
      .tickPadding(10);
    
    const yAxisG = g.append('g').call(yAxis);
    yAxisG.selectAll('.domain').remove();
    
    yAxisG.append('text')
        .attr('class', 'axis-label')
        .attr('y', -60)
        .attr('x', -innerHeight / 2)
        .attr('fill', 'black')
        .attr('transform', `rotate(-90)`)
        .attr('text-anchor', 'middle')
        .text(yAxisLabel);
    
    const xAxisG = g.append('g').call(xAxis)
      .attr('transform', `translate(0,${innerHeight})`);
    
    xAxisG.select('.domain').remove();
    
    /*xAxisG.append('text')
        .attr('class', 'axis-label')
        .attr('y', 80)
        .attr('x', innerWidth / 2)
        .attr('fill', 'black')
        .text(xAxisLabel);
    */

    const colorValue = ['nb_cdi_actifs',
        'ETP_cdiactifs', 
        'ETP_budgetHRZ_cdiactifs'];
        
    const colorScale = d3.scaleOrdinal(d3.schemeCategory10).domain(colorValue);  
          
    const lineGenerator = d3.line()
      .x(d => xScale(xValue(d)))
      .y(d => yScale(yValue(d)))
      .curve(d3.curveBasis);

    g.append('path')
        .attr('class', 'line-path')
        .attr('d', lineGenerator(data))
        .attr('stroke', colorScale('nb_cdi_actifs'));

    const lineGeneratoryValueetpcdi = d3.line()
        .x(d => xScale(xValue(d)))
        .y(d => yScale(yValueetpcdi(d)))
        .curve(d3.curveBasis);
    
    g.append('path')
          .attr('class', 'line-path')
          .attr('d', lineGeneratoryValueetpcdi(data))
          .attr('stroke', colorScale('ETP_cdiactifs'));

    const lineGeneratoryValueetpbudget = d3.line()
        .x(d => xScale(xValue(d)))
        .y(d => yScale(yValueetpbudget(d)))
        .curve(d3.curveBasis);

    g.append('path')
          .attr('class', 'line-path')
          .attr('d', lineGeneratoryValueetpbudget(data))
          .attr('stroke', colorScale('ETP_budgetHRZ_cdiactifs'));
    
    g.append('text')
        .attr('class', 'title')
        .attr('y', -10)
        .text(title);

/*
        ///tooltip 
    var tooltip = d3.select("#svg1").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    g.selectAll(".dot")
          .data(data)
        .enter().append("circle")
          .attr("class", "dot")
          .attr("r", 3.5)
          .attr("cx", d => xScale(xValue(d)))
          .attr("cy", d => yScale(yValue(d)))
          .style("fill", "black")//function(d) { return color(cValue(d));}) 
          .on("mouseover", function(d) {
            console.log(yValue(d))
            
              tooltip.transition()
                  .duration(200)
                  .style("opacity", .9);
              tooltip.html("<br/> (" + xValue(d) 
              + ", " + yValue(d) + ")")
                  .style("background-color", "black")
                  .style("left", (d3.event.pageX + 5) + "px")
                  .style("top", (d3.event.pageY - 28) + "px")
                  .style("width",'200px')
                  .style("height",'28px');
            console.log(tooltip)
            console.log('height',tooltip.style)
          })
          .on("mouseout", function(d) {
              tooltip.transition()
                  .duration(500)
                  .style("opacity", 1);
          });
*/
    svg.append('g')
            .attr('transform', `translate(775,150)`)
            .call(colorLegend, {
              colorScale,
              circleRadius: 10,
              spacing: 50,
              textOffset: 20
            });


    //création interractivité mouseover
    

  var mouseG = svg.append("g")
    .attr("class", "mouse-over-effects");

  mouseG.append("path") // this is the black vertical line to follow mouse
    .attr("class", "mouse-line")
    .style("stroke", "black")
    .style("stroke-width", "1px")
    .style("opacity", "0")
    .attr('transform', `translate(${margin.left},${margin.top})`);
    
  var lines = document.getElementsByClassName('line-path');

  let cities = colorScale.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {
          date: xValue(d),
          nb_cdi_actifs: yValue(d) ,
          ETP_cdiactifs: yValueetpcdi(d) ,
          ETP_budgetHRZ_cdiactifs : yValueetpbudget(d) 
        };
      })
    };
  });

  var mousePerLine = mouseG.selectAll('.mouse-per-line')
    .data(cities)
    .enter()
    .append("g")
    .attr("class", "mouse-per-line");

  mousePerLine.append("circle")
    .attr("r", 7)
    .style("stroke", function(d) {
      return colorScale(d.name);
    })
    .style("fill", "none")
    .style("stroke-width", "1px")
    .style("opacity", "0")
    .attr('transform', `translate(${margin.left},${margin.top})`);

  mousePerLine.append("text")
    .attr("transform", "translate(10,3)")
    .attr('transform', `translate(${margin.left +10},${margin.top -10})`);;

    //on crée un rect invisible où la yline se déplace
  mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
    .attr('width', innerWidth) // can't catch mouse events on a g element
    .attr('height', innerHeight)
    .attr('fill', 'none') 
    .attr('pointer-events', 'all')
    .attr('transform', `translate(${margin.left},${margin.top})`)
    .on('mouseout', function() { // on mouse out hide line, circles and text
      d3.select(".mouse-line")
        .style("opacity", "0");
      d3.selectAll(".mouse-per-line circle")
        .style("opacity", "0");
      d3.selectAll(".mouse-per-line text")
        .style("opacity", "0");
    })
    .on('mouseover', function() { // on mouse in show line, circles and text
      d3.select(".mouse-line")
        .style("opacity", "1");
      d3.selectAll(".mouse-per-line circle")
        .style("opacity", "1");
      d3.selectAll(".mouse-per-line text")
        .style("opacity", "1")
    })
    .on('mousemove', function() { // mouse moving over canvas
      var mouse = d3.mouse(this); //renvoie array de la pos de la souris avec mouse[0]=x et mouse[1]=y
      d3.select(".mouse-line")
        .attr("d", function() {
          var d = "M" + mouse[0] + "," + innerHeight;
          d += " " + mouse[0] + "," + 0;

          return d;
        });

        //gestion déplacement de la yline
      d3.selectAll(".mouse-per-line")
        .attr("transform", function(d, i) {
          
          
          var xDate = xScale.invert(mouse[0]),
              bisect = d3.bisector(function(d) { return d.date; }).right;
              idx = bisect(d.values, xDate);
          
          var beginning = 0,
              end = lines[i].getTotalLength(),
              target = null;

          //quand arrêter d'afficher la ligne
          while (true){
            target = Math.floor((beginning + end) / 2);
            pos = lines[i].getPointAtLength(target); //svgpoint {x:,y:}
            
            if ((target === end || target === beginning) && pos.x !== mouse[0]) {
                break;
            }
            if (pos.x > mouse[0])      end = target;
            else if (pos.x < mouse[0]) beginning = target;
            else break; //position found
          }
        

          d3.select(this).select('text')
            .text(yScale.invert(pos.y).toFixed(2));
            //.text(d.values[xScale.invert(pos.x).getMonth()][d.name].toFixed(2));
          
          return "translate(" + mouse[0] + "," + pos.y +")";
        });
        
    });
};
//url trouvable dans init.py et index.html
d3.dsv(";","."+url_resemploigraph).then(data => 
	{
  console.log('data',data)

  let datestringtodate = function(chaine) {return new Date(chaine.slice(0,4) + '-' + chaine.slice(4)) ;};

  data.forEach(d => {

    d.nb_cdi_actifs = +d.nb_cdi_actifs
    d.date = datestringtodate(d.date)

    d.ETP_cdiactifs = +d.ETP_cdiactifs

    d.ETP_budgetHRZ_cdiactifs = +d.ETP_budgetHRZ_cdiactifs 

    d.cumul_depuis_jan_recrutements_externes = +d.cumul_depuis_jan_recrutements_externes
    d.cumul_depuis_jan_mobilites_entrantes = +d.cumul_depuis_jan_mobilites_entrantes
    d.cumul_depuis_jan_reintegrations = +d.cumul_depuis_jan_reintegrations

    d.cumul_depuis_jan_retraites_departdef = -d.cumul_depuis_jan_retraites_departdef
    d.cumul_depuis_jan_mobilites_sortantes = -d.cumul_depuis_jan_mobilites_sortantes
    d.cumul_depuis_jan_sorties_provisoires = -d.cumul_depuis_jan_sorties_provisoires

    d.mobilites_entrantes = +d.mobilites_entrantes
    d.mobilites_sortantes = -d.mobilites_sortantes
  });
  render(data)

  // deuxième ligne

  const yValuecumul_depuis_jan_recrutements_externes = d => d.cumul_depuis_jan_recrutements_externes
  const yValuecumul_depuis_jan_mobilites_entrantes = d => d.cumul_depuis_jan_mobilites_entrantes
  const yValuecumul_depuis_jan_reintegrations = d => d.cumul_depuis_jan_reintegrations

  const yValuecumul_depuis_jan_retraites_departdef = d=>d.cumul_depuis_jan_retraites_departdef
  const yValuecumul_depuis_jan_mobilites_sortantes = d=>d.cumul_depuis_jan_mobilites_sortantes
  const yValuecumul_depuis_jan_sorties_provisoires = d=>d.cumul_depuis_jan_sorties_provisoires
      
  const xValue = d => d.date
  const margin = { top: 60, right: 200, bottom: 88, left: 105 };

  const svg2 = d3.select('#svg2');
  barChart(data,svg2, margin, xValue, yValuecumul_depuis_jan_recrutements_externes, 'Recrutement externe accumulé', 70, show_objectif=false);

  const svg3 = d3.select('#svg3');
  barChart(data,svg3, margin, xValue, yValuecumul_depuis_jan_mobilites_entrantes, 'Mobilités rentrantes accumulées', 624, show_objectif=false);

  const svg4 = d3.select('#svg4');
  barChart(data,svg4, margin, xValue, yValuecumul_depuis_jan_reintegrations, 'Réintégrations accumulées',121, show_objectif=false);

  const svg5 = d3.select('#svg5');
  barChart(data,svg5, margin, xValue, yValuecumul_depuis_jan_retraites_departdef, 'Départ retraite accumulé',646, show_objectif=false);

  const svg6 = d3.select('#svg6');
  barChart(data,svg6, margin, xValue, yValuecumul_depuis_jan_mobilites_sortantes, 'Mobilités sortantes accumulées',541, show_objectif=false);

  const svg7 = d3.select('#svg7');
  barChart(data,svg7, margin, xValue, yValuecumul_depuis_jan_sorties_provisoires, 'Sorties provisoires accumulées',140, show_objectif=false);

  const svg9 = d3.select('#svg9');
  groupedBarchart(data,svg9,margin, xValue, 'Mobilités entrantes - Mobilités sortantes 2019');

  //groupedBarchart(data,svg9,margin, xValue, 'Mobilités entrantes - Mobilités sortantes 2019');
    
});

//d3.dsv(";", String.raw `./data/recrutement_externe.csv`, {data: "text/plain", charset: "UTF-8"},).then(
d3.dsv(";", url_recrutement_externe, {data: "text/plain", charset: "UTF-8"},).then(
  data => {
      tabulate(html_element='#tabrecext',data, data.columns);
  }
)
/*
d3.dsv(";", String.raw `./data/recrutement_externe.csv`, {data: "text/plain", charset: "UTF-8"},).then(
  data => {
      tabulate(data, data.columns);
  }
)
  */
  
//d3.dsv(';','./data/effectifparentite.csv').then(data=>{
d3.dsv(';',url_effectifparentite).then(data=>{
  console.log('effectif',data)
  let nbcdi =0
  let nbcdd =0
  let nbalt =0
  data.forEach(d => {
    let valcdiper = (+d['cdi percent'])
    let valcddper = (+d['cdd percent'])
    let valaltper = (+d['alt percent'])
    let valeffectif = (+d['effectif um'])
    d['cdi percent'] = d3.format(".2r")(valcdiper)
    d['cdd percent'] = d3.format(".2r")(valcddper)
    d['alt percent'] = d3.format(".2r")(valaltper)
    d['effectif um'] = valeffectif

    nbcdi += valcdiper*valeffectif
    nbcdd += valcddper*valeffectif
    nbalt += valaltper*valeffectif

  });

  const svg8 = d3.select('#svg8');
  /*
  let nbcdi = data.map(row => (row['effectif um']*(+row['cdi percent']))/100)
                    .reduce((accumulator, currentValue) => accumulator + currentValue);
  
  let nbcdd = data.map(row => (row['effectif um']*(+row['cdd percent']))/100)
                    .reduce((accumulator, currentValue) => accumulator + currentValue);

  let nbalt = data.map(row => (row['effectif um']*(+row['alt percent']))/100)
                    .reduce((accumulator, currentValue) => accumulator + currentValue);
  */
  //console.log(nbcdi)
  document.getElementById('nbcdi').innerHTML = (nbcdi/100).toFixed(0);
  document.getElementById('nbcdd').innerHTML = (nbcdd/100).toFixed(0);
  document.getElementById('nbalt').innerHTML = (nbalt/100).toFixed(0);
  stackedbarchart(data, svg8);
});


let map = () =>{
  const width = 850, 
      height = 800,
      colors = ['#d4eac7', '#c6e3b5', '#b7dda2', '#a9d68f', '#9bcf7d', '#8cc86a', '#7ec157', '#77be4e', '#70ba45', '#65a83e', '#599537', '#4e8230', '#437029', '#385d22', '#2d4a1c', '#223815'];
  
  const path = d3.geoPath();
  
  const projection = d3.geoMercator()
      .center([2.454071, 46.279229])
      .scale(3000)
      .translate([width / 2, height / 2]);
  
  path.projection(projection);
  
  const svg = d3.select('#map').append("svg")
      .attr("id", "svg")
      .attr("width", width)
      .attr("height", height)
      .attr("class", "Blues")
  
  svg.append("text")
      .attr("x", (width / 2))
      .attr("y", 15)
      .attr("text-anchor", "middle")
      .style("fill", "#857567")
      .style("font-weight", "300")
      .style("font-size", "16px")
      .text("Effectif par site DEF et Taux de chômage par département");
  
  // Append the group that will contain our paths
  const deps = svg.append("g");
  
  
  var promises = [];
  /*
  promises.push(d3.json('./data/departements.geojson'));
  //promises.push(d3.csv("./data/population.csv"));
  promises.push(d3.dsv(";","./data/effectifparregion4.csv"));
  promises.push(d3.dsv(";","./data/donnees_insee_poleemploi.csv"))
  */

  promises.push(d3.json(url_departements));
  //promises.push(d3.csv("./data/population.csv"));
  promises.push(d3.dsv(";",url_effectifparregion));
  promises.push(d3.dsv(";",url_donnees_insee_poleemploi))
  
  Promise.all(promises).then(function(values) {
      const geojson = values[0]; // Récupération de la première promesse : le contenu du fichier JSON
      const csv = values[1];
      const insee = values[2]
              
      //const geojson = getDepartments();
      //const csv = getPopulations();
  
      console.log(csv)
      console.log(geojson)
      console.log(geojson.features)
      console.log(insee)
  
      var features = deps
          .selectAll("path")
          .data(geojson.features)
          .enter()
          .append("path")
          .attr('id', function(d) {return "d" + d.properties.code;})
          .attr("d", path);
  
      var quantile = d3.scaleQuantile()
          //.domain([0, d3.max(csv, function(e) { return +e.POP; })])
          .domain([0, d3.max(insee, function(e) { return +e.tx_chomage; })])
          .range(colors);
  
      var legend = svg.append('g')
          .attr('transform', 'translate(725, 150)')
          .attr('id', 'legend');
          
      legend.selectAll()
              .data(d3.range(colors.length))
              .enter().append('svg:rect')
                  .attr('height', '20px')
                  .attr('width', '20px')
                  .attr('x', 5)
                  .attr('y', function(d) { return d * 20; })
                  .style("fill", function(d) { return colors[d]; });
                  
      var legendScale = d3.scaleLinear() // écarts trop grands changer de scale, mais log enlève la légende
          //.domain([0, d3.max(csv, function(e) { return +e.POP; })])
          .domain([0, d3.max(insee, function(e) { return +e.tx_chomage; })])
          .range([0, colors.length * 20]);
              
      var legendAxis = svg.append("g")
          .attr('transform', 'translate(750, 150)')
          .call(d3.axisRight(legendScale).ticks(12));
              
      /*
      csv.forEach(function(e,i) {
          d3.select("#d" + e.CODE_DEPT)
              .style("fill", function(d) { return quantile(+e.POP); })
              .on("mouseover", function(d) {
                  d3.select("#d" + e.CODE_DEPT).style('fill',"#9966cc");
                  div.transition()        
                      .duration(200)      
                      .style("opacity", .9);
                  div.html("<b>Région : </b>" + e.NOM_REGION + "<br>"
                          + "<b>Département : </b>" + e.NOM_DEPT + "<br>"
                          + "<b>Population : </b>" + e.POP + "<br>")
                      .style("left", (d3.event.pageX + 30) + "px")     
                      .style("top", (d3.event.pageY - 30) + "px");
              })
              .on("mouseout", function(d) {
                  d3.select("#d" + e.CODE_DEPT).style("fill", function(d) { return quantile(+e.POP); })
                  div.style("opacity", 0);
                  div.html("")
                      .style("left", "-500px")
                      .style("top", "-500px");
              });
      });
      */
  
     insee.forEach(function(e,i) {
      d3.select("#d" + e.code)
          .style("fill", function(d) { return quantile(+e.tx_chomage); })
          .on("mouseover", function(d) {
              d3.select("#d" + e.code).style('fill',"#9966cc");
              div.transition()        
                  .duration(200)      
                  .style("opacity", .9);
              div.html("<b>Nb chômeurs cat A : </b>" + e.A + "<br>"
                      + "<b>Département : </b>" + e.nom_dpt + "<br>"
                      + "<b>Taux de chômage : </b>" + parseFloat(e.tx_chomage).toFixed(1)+ "%" + "<br>")
                  .style("left", (d3.event.pageX + 30) + "px")     
                  .style("top", (d3.event.pageY - 30) + "px");
          })
          .on("mouseout", function(d) {
              d3.select("#d" + e.code).style("fill", function(d) { return quantile(+e.tx_chomage); })
              div.style("opacity", 0);
              div.html("")
                  .style("left", "-500px")
                  .style("top", "-500px");
          });
      });
  
      // Append a DIV for the tooltip
      var div = d3.select("#map").append("div")   
          .attr("class", "tooltip")               
          .style("opacity", 0);
  
      // create a tooltip
      var Tooltip = d3.select("#map")
        .append("div")
        .attr('id', 'infoshover')
        .attr("class", "tooltip")
        .style("opacity", 1)
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "2px")
        .style("border-radius", "5px")
        .style("padding", "5px")
        .style('background-color',"#A53030")
        //.text("haha")
  
      // Three function that change the tooltip when user hover / move / leave a cell
      var mouseover = function(d) {
        Tooltip.style("opacity", 1)
      }
      var mousemove = function(d) {
        Tooltip
          .html( "site: " + d.site + "<br>" + "<b>Nb employés ville: </b>" + d.POP + "<br>")
          .style("left", (d3.event.pageX + 30) + "px")
          .style("top", (d3.event.pageY - 30) + "px")
      
        //console.log('tooltip',d3.mouse(Tooltip.node())) positions bizarres, pourquoi?
      }
  
      var mouseleave = function(d) {
        Tooltip.style("opacity", 0)
      }
  
      // Add circles:
      let radius = d3.scaleSqrt()
          .domain([0, 2000])
          .range([5, 30]);
  
      svg.selectAll("myCircles")
          .data(csv)
          .enter()
          .append("circle")
          .attr("cx", function(d){ return projection([+d.gps_lng, +d.gps_lat])[0] })
          .attr("cy", function(d){ return projection([+d.gps_lng, +d.gps_lat])[1] })
          .attr("r", function(d){ return radius(+d.POP)})
          .attr("class", "circle")
          .style("fill", "69b3a2")
          .attr("stroke", "#69b3a2")
          .attr("stroke-width", 0.5)
          .attr("fill-opacity", .4)
          .on('mouseover', (d) => mouseover(d))
          .on('mousemove', (d) => mousemove(d))
          .on('mouseleave', (d) => mouseleave(d))
      });
  }
  map()