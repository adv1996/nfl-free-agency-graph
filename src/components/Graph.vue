<template>
  <v-app dark>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>NFL Free Agency</span>
      </v-toolbar-title>
      <v-spacer/>
      <v-btn right outline color="yellow" @click="desktopLegend">{{isLegend}}</v-btn>
    </v-toolbar>
    <v-content>
      <v-container fill-height="true">
        <v-layout
          text-xs-center
          wrap
        >
          <v-flex xs12>
            <svg :height="height" :width="width" id="teams">
              <g id="legend"/>
              <g class="everything">
                <g class="links"></g>
                <g class="nodes"></g>
              </g>
            </svg>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
  /* eslint-disable */
  import * as d3 from 'd3';
  import TestData from '../../data.json'
  export default {
    data() {
      return {
        height: 0,
        width: 0,
        left: 20,
        right: 20,
        top: 20,
        bottom: 20,
        radius: 350,
        codes: [true,true,true],
        isLegend: 'Enable Legend',
      }
    },
    mounted() {
      this.setDimensions()
    },
    methods: {
      desktopLegend() {
        if (this.isLegend === 'Disable Legend') {
          d3.select('#legend')
            .transition()
            .duration(1000)
            .style('opacity', 0)
          this.isLegend = 'Enable Legend'
        } else {
          d3.select('#legend')
            .transition()
            .duration(1000)
            .style('opacity', 1)
          this.isLegend = 'Disable Legend'
        }
      },
      setDimensions() {
        this.width = this.$el.offsetWidth
        this.height = this.$el.offsetHeight
        this.createGraph();
        this.createLegend();
      },
      createLegend() {
        let legends = [
          {
            'type': 'rectangle',
            'color': '#73C2FB',
            'content': 'Team'
          },
          {
            'type': 'circle',
            'color': '#deebf7',
            'content': 'Player'
          },
          {
            'type': 'line',
            'color': '#CA3433',
            'content': 'Player Leaving',
            'status': true,
            'code': 0,
          },
          {
            'type': 'line',
            'color': '#D5B85A',
            'content': 'Player Joining',
            'status': true,
            'code': 1,
          },
          {
            'type': 'line',
            'color': '#0080FE',
            'content': 'Player Staying',
            'status': true,
            'code': 2,
          }
        ]
        let ys = d3.scaleLinear().domain([0,5]).range([0, 110])

        d3.select('#legend')
          .append('rect')
            .attr('height', 120)
            .attr('width', 230)
            .attr('x', 10)
            .attr('y', 10)
            .attr('fill', '#D9DDDC')
            .attr('rx', 10)
            .attr('ry', 10)
        for (let i = 0; i < legends.length; i++) {
          if (legends[i].type === 'rectangle') {
            d3.select('#legend')
              .append('rect')
              .attr('height', 25)
              .attr('width', 25)
              .attr('x', 50)
              .attr('y', ys(i) + 12.5)
              .attr('fill', legends[i].color)
              .attr('rx', 6)
              .attr('ry', 6)
          }
          if (legends[i].type === 'circle') {
            d3.select('#legend')
              .append('circle')
              .attr('r', 10)
              .attr('cx', 62.5)
              .attr('cy', ys(i) + 27.5)
              .attr('fill', legends[i].color)
          }
          if (legends[i].type === 'line') {
            d3.select('#legend')
              .append('rect')
              .attr('x', 30)
              .attr('y', ys(i) + 20)
              .attr('width', 60)
              .attr('height', 5)
              .attr('fill', legends[i].color)
          }
          d3.select('#legend')
            .append('text')
            .attr('x', 150)
            .attr('y', ys(i))
            .attr('dy', 25)
            .text(legends[i].content)
            .attr("text-anchor", "right")  
            .style("font-size", "14px")
        }
        let that = this;
        let g = d3.select('#legend')
          .selectAll('.toggle')
          .data(legends.filter((d) => {
            if (d.type === 'line') {
              return true
            }
            return false
          }))
          .enter()
          .append('g')
        g.append('rect')
          .attr('x', 208)
          .attr('y', (d,i) => {
            return ys(i + 2) + 12.5
          })
          .attr('width', 25)
          .attr('height', 15)
          .attr('fill', 'black')
          .attr('rx', 6)
          .attr('ry', 6)
          .style('fill-opacity', 0.7)

        g.append('circle')
          .attr('cx', 215)
          .attr('cy', (d, i) => {
            return ys(i + 2) + 20
          })
          .attr('r', 6)
          .attr('fill', (d) => {
            return d.status ? d.color : 'white'
          })
          .attr('stroke-width', '2px')
          .on('click', function(d) {
            if (that.codes[d.code]) {
              d3.select(this)
                .transition()
                .duration(1000)
                .attr('fill', 'white')
                .attr('cx', 225)
              d3.selectAll('.link' + d.code)
                .transition()
                .duration(1000)
                .style("stroke-opacity", .1);
              that.codes[d.code] = !that.codes[d.code]    
            } else {
              d3.select(this)
                .transition()
                .duration(1000)
                .attr('fill', d.color)
                .attr('cx', 215)
              d3.selectAll('.link' + d.code)
                .transition()
                .duration(1000)
                .style("stroke-opacity", 1);
              that.codes[d.code] = !that.codes[d.code]
            }
          })
        
        d3.select('#legend')
          .style('opacity', 0)
      },
      createGraph() {
        let that = this;
        let tooltip = d3.select('body')
          .append('div')
          .attr('class', 'tooltip')	

        var zoom_handler = d3.zoom()
          .on("zoom", zoom_actions);
        zoom_handler(d3.select('#teams')); 

        function zoom_actions(){
          d3.select('.everything').attr("transform", d3.event.transform)
        }
        
        var simulation = d3.forceSimulation(TestData.nodes)
          .force('charge', d3.forceManyBody().strength(-100))
          .force("collide", d3.forceCollide(75).strength(1))
          .force('center', d3.forceCenter(this.width / 2, this.height / 2))
          .force('link', d3.forceLink().links(TestData.links).distance(25))
          .on('tick', ticked);
        simulation.tick(300);
        // nearest neighbor
        function drag(simulation) {
          
          function dragstarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          }
          
          function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
          }
          
          function dragended(d) {
            if (!d3.event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          }
          
          return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
        }
        const linkedByIndex = {};
        TestData.links.forEach(d => {
          linkedByIndex[`${d.source.index},${d.target.index}`] = 1;
        });

        function isConnected(a, b) {
          return linkedByIndex[`${a.index},${b.index}`] || linkedByIndex[`${b.index},${a.index}`] || a.index === b.index;
        }

        function updateLinks() {
          let u = d3.select('.links')
            .selectAll('line')
            .data(TestData.links)

          u.enter()
            .append('line')
            .merge(u)
            .attr('x1', function(d) {
              return d.source.x
            })
            .attr('y1', function(d) {
              return d.source.y
            })
            .attr('x2', function(d) {
              return d.target.x
            })
            .attr('y2', function(d) {
              return d.target.y
            })
            .attr('class', (d) => {
              return 'link' + d.status
            })
            .style("stroke", (d) => {
              if (d.status === 0) {
                return '#CA3433'
              } else if (d.status === 1) {
                return '#D5B85A'
              } else {
                return '#0080FE'
              }
              return d.status
            })

          u.exit().remove()
        }

        function fade(d) {
          d3.selectAll('.cnode')
            .attr('fill-opacity', function(o) {
              const connected = isConnected(d, o) ? 1 : false;
              this.setAttribute('stroke', connected ? '#3182bd' : 0)
              return connected ? 1 : .1;
            })
          d3.selectAll('.rnode')
            .attr('fill-opacity', function(o) {
              const connected = isConnected(d, o) ? 1 : false;
              return connected ? 1 : .1;
            })
          d3.selectAll('line')
            .style("stroke-opacity", function(o) {
              if (o.source.index === d.Index || o.target.index === d.Index) {
                return 1;
              } else {
                return .1
              }
          });

        }
        function fadeOut() {
          d3.selectAll('.cnode')
            .attr('fill-opacity', 1)
            .attr('stroke', '#598BAF')
            .attr('stroke-width', '5px')
          d3.selectAll('.link0')
            .style('stroke-opacity', that.codes[0] ? 1 : .1)
          d3.selectAll('.link1')
            .style('stroke-opacity', that.codes[1] ? 1 : .1)
          d3.selectAll('.link2')
            .style('stroke-opacity', that.codes[2] ? 1 : .1)
          d3.selectAll('.rnode')
            .attr('fill-opacity', 1)
        }
        
        function updateNodes() {
          let u = d3.select('.nodes')
            .selectAll('circle')
            .data(TestData.nodes.filter((d) => {return d.Type === 'Player'}))
          u.enter()
            .append('circle')
              .merge(u)
              .attr('class', 'cnode')
              .attr('cx', (d) => {return d.x})
              .attr('cy', (d) => {return d.y})
              .attr('r', (d) => {
                let millions = d.Value / 100000
                return Math.sqrt(millions) * 3
              })
              .attr('fill', (d) => {
                return '#deebf7'
              })
              .on('mouseover', (d) => {
                tooltip
                  .style("left", (d3.event.pageX + 15) + "px")	
                  .style("top", (d3.event.pageY - 28) + "px")
                  .style('opacity', 1)
                  .style('height', (e) => {
                    if (d.Name.length > 13) {
                      return 50;
                    } else {
                      return 60;
                    }
                  })
                  .html(
                    d.Name + '<br/>' + d.Pos + '<br/>' + '$' + (d.Value / 1000000).toFixed(1) + ' Million'
                  )
                fade(d)
              })
              .on('mouseout', (d) => {
                tooltip
                  .style('opacity', 0)
                fadeOut()
              })

          u.exit().remove()
          u = d3.select('.nodes')
            .selectAll('rect')
            .data(TestData.nodes.filter((d) => {return d.Type === 'Team'}))

          u.enter()
            .append('rect')
              .merge(u)
              .attr('width', 60)
              .attr('height', 60)
              .attr('x', (d) => {return d.x - 60 / 2})
              .attr('y', (d) => {return d.y - 60 / 2})
              .attr('fill', '#73C2FB')
              .attr('class', 'rnode')
              .on('mouseover', (d) => {
                fade(d)
              })
              .on('mouseout', (d) => {
                fadeOut()
              })
              .attr("rx", 6)
              .attr("ry", 6)
          u.exit().remove()

          u = d3.select('.nodes')
            .selectAll('image')
            .data(TestData.nodes.filter((d) => {return d.Type === 'Team'}))

          u.enter()
            .append('image')
              .merge(u)
              .attr('xlink:href', (d) => {
                return 'https://static.nfl.com/static/site/img/logos/svg/teams/' + d.Name + '.svg'
              })
              .attr('width', 50)
              .attr('height', 50)
              .attr('x', (d) => {return d.x - 50 / 2})
              .attr('y', (d) => {return d.y - 50 / 2})
              .on('mouseover', (d) => {
                fade(d)
              })
              .on('mouseout', (d) => {
                fadeOut()
              })

          u.exit().remove()

          u = d3.select('.nodes')
            .selectAll('text')
            .data(TestData.nodes.filter((d) => {return d.Value > 3000000 && d.Type === 'Player'}))

          u.enter()
            .append('text')
              .merge(u)
              .text((d) => {
                return d.Pos.replace(/[0-9]/g, '');
              })
              .attr('x', (d) => {return d.x})
              .attr('y', (d) => {return d.y})
              .attr('dy', (d) => {
                return 5
              })
              .on('mouseover', (d) => {
                tooltip
                  .style("left", (d3.event.pageX + 10) + "px")		
                  .style("top", (d3.event.pageY - 28) + "px")
                  .style('opacity', 1)
                  .html(
                    d.Name + '<br/>' + d.Pos + '<br/>' + '$' + (d.Value / 1000000).toFixed(1) + ' Million'
                  )
                fade(d)
              })
              .on('mouseout', (d) => {
                tooltip
                  .style('opacity', 0)
                fadeOut()
              })
          u.exit().remove()
        }

        function ticked() {
          updateLinks()
          updateNodes()
        }
      }
    }
  }
</script>

<style>
line {
  stroke-width: 5px;
}
text {
  text-anchor: middle;
  font-family: "Helvetica Neue", Helvetica, sans-serif;
  fill: #666;
  font-size: 16px;
}
div.tooltip {	
  position: absolute;
  text-align: center;
  width: 90px;			
  padding: 2px;				
  font-size: 12px;		
  font-family: "Helvetica Neue", Helvetica, sans-serif;
  color: black;
  background:#88b8e6;	
  border: 0px;		
  border-radius: 8px;			
  pointer-events: none;			
}
div.legend_area {
  position: absolute;	
  width: 200px;					
  height: 150px;	
}
#legend {
  z-index: 200;
}
</style>
