<template>
  <v-app dark>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>NFL Free Agency</span>
      </v-toolbar-title>
      <v-spacer/>
      <v-btn right outline color="yellow" @click="desktopLegend">{{isLegend}}</v-btn>
      <!-- <a href="https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Fdeveloper.twitter.com%2Fen%2Fdocs%2Ftwitter-for-websites%2Ftweet-button%2Foverview&amp;ref_src=twsrc%5Etfw&amp;text=NFL%20Free%20Agency%Graph&amp;tw_p=tweetbutton&amp;url=https%3A%2F%2Fdeveloper.twitter.com%2Fen%2Fdocs%2Ftwitter-for-websites%2Ftweet-button%2Foverview.html" class="btn" id="b">
        <v-btn right outline color="blue">Share on Twitter!</v-btn>
      </a> -->
      
      <a class="twitter-share-button"
        href="https://twitter.com/intent/tweet?url=https%3a%2f%2fnfl-fa-2019.surge.sh%2f"
        data-size="large">
        <v-btn
          color="blue"
          flat
          outline 
        >
          <font-awesome-icon :icon="['fab', 'twitter']" size="lg"/>
        </v-btn>
      </a>
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
  import { sliderBottom } from 'd3-simple-slider';
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
        linkedByIndex: [],
        val: [7,25],
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
        let ys = d3.scaleLinear().domain([0,5]).range([10, 110])
        let tooltip = d3.select('body')
          .append('div')
          .attr('class', 'tooltip')	
          .style('opacity', 0)

        d3.select('#legend')
          .append('rect')
            .attr('height', 185)
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
              .attr('y', ys(i) + 2.5)
              .attr('fill', legends[i].color)
              .attr('rx', 6)
              .attr('ry', 6)
          }
          if (legends[i].type === 'circle') {
            d3.select('#legend')
              .append('circle')
              .attr('r', 10)
              .attr('cx', 62.5)
              .attr('cy', ys(i) + 22)
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
            .attr('class', 'legendText')
            .attr('x', 100)
            .attr('y', ys(i))
            .attr('dy', 25)
            .text(legends[i].content)
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
        let slider = sliderBottom()
          .min(0)
          .max(25)
          .width(150)
          .ticks(5)
          .default(that.val)
          .fill('#2196f3')
          .step(1)
          .handle(
            d3
              .symbol()
              .type(d3.symbolCircle)
              .size(150)()
          )
          .on('onchange', val => {
            that.updateNodes(val)
            that.updateLinks(val)
          })
        d3.select('#legend').append('text')
          .attr('x', 20)
          .attr('y', 137)
          .text('Filter Players by Salary (millions)')
          .attr('class', 'filterText')
        d3.select('#legend').append('g')
          .attr('transform', 'translate(45,150)')
          .call(slider)
        d3.select('#legend')
          .style('opacity', 0)
      },
      createGraph() {
        let that = this;
        // zoom functionality
        let zoom_handler = d3.zoom()
          .on("zoom", zoom_actions);
        zoom_handler(d3.select('#teams')); 
        
        function zoom_actions(){
          d3.select('.everything').attr("transform", d3.event.transform)
        }
        let transform = d3.zoomIdentity.translate(that.width / 2, that.height / 2).scale(.25);
        d3.select('.everything')
          .attr("transform", transform)

        
        var simulation = d3.forceSimulation(TestData.nodes)
          .force('charge', d3.forceManyBody().strength(-100))
          .force("collide", d3.forceCollide(75).strength(1))
          .force('center', d3.forceCenter(this.width / 2, this.height / 2))
          .force('link', d3.forceLink().links(TestData.links).distance(25))
          .on('tick', ticked);
        simulation.tick(300)
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
        that.linkedByIndex = {};
        TestData.links.forEach(d => {
          that.linkedByIndex[`${d.source.index},${d.target.index}`] = 1;
        });
        function ticked() {
          that.updateLinks(that.val)
          that.updateNodes(that.val)
        }
      },
      updateLinks(val) {
        let that = this;
        let filteredNodes = TestData.links.filter((d) => {
          if (d.value >= val[0] * 1000000 && d.value <= val[1] * 1000000) {
            return true
          } else {
            return false;
          }
        })
        let u = d3.select('.links')
          .selectAll('line')
          .data(filteredNodes)
        u.exit().remove()

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
          .style('stroke-opacity', (d) => {
            if (that.codes[d.status]) {
              return 1
            } else {
              return .1
            }
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
      },
      isConnected(a, b) {
        return this.linkedByIndex[`${a.index},${b.index}`] || this.linkedByIndex[`${b.index},${a.index}`] || a.index === b.index;
      },
      fadeOut() {
        let that = this;
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
      },
      fade(d) {
        let that = this
        d3.selectAll('.cnode')
          .attr('fill-opacity', function(o) {
            const connected = that.isConnected(d, o) ? 1 : false;
            this.setAttribute('stroke', connected ? '#3182bd' : 0)
            return connected ? 1 : .1;
          })
        d3.selectAll('.rnode')
          .attr('fill-opacity', function(o) {
            const connected = that.isConnected(d, o) ? 1 : false;
            return connected ? 1 : .1;
          })
        d3.selectAll('.link0')
          .style("stroke-opacity", function(o) {
            if (o.source.index === d.Index || o.target.index === d.Index) {
              return 1;
            } else {
              return .1
            }
        });
        d3.selectAll('.link1')
          .style("stroke-opacity", function(o) {
            if (o.source.index === d.Index || o.target.index === d.Index) {
              return 1;
            } else {
              return .1
            }
        });
        d3.selectAll('.link2')
          .style("stroke-opacity", function(o) {
            if (o.source.index === d.Index || o.target.index === d.Index) {
              return 1;
            } else {
              return .1
            }
        });
      },
      updateNodes(val) {
        let that = this;
        let tooltip = d3.select('.tooltip')
        let filteredNodes = TestData.nodes.filter((d) => {
          if (d.Type === 'Player') {
            if (d.Value >= val[0] * 1000000 && d.Value <= val[1] * 1000000) {
              return true
            } else {
              return false;
            }
          }
          return true;
        })
        let u = d3.select('.nodes')
          .selectAll('circle')
          .data(filteredNodes.filter((d) => {return d.Type === 'Player'}))
        u.exit().remove()
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
              let money = d.Value
              if (money === 666666) {
                money = 'Unknown'
              } else {
                money = (money / 1000000).toFixed(1)
                money = '$' + money + ' Million'
              }
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
                  d.Name + '<br/>' + d.Pos + '<br/>' + money
                )
              that.fade(d)
            })
            .on('mouseout', (d) => {
              tooltip
                .style('opacity', 0)
              that.fadeOut()
            })

        u.exit().remove()
        u = d3.select('.nodes')
          .selectAll('rect')
          .data(filteredNodes.filter((d) => {return d.Type === 'Team'}))

        u.enter()
          .append('rect')
            .merge(u)
            .attr('width', 80)
            .attr('height', 80)
            .attr('x', (d) => {return d.x - 80 / 2})
            .attr('y', (d) => {return d.y - 80 / 2})
            .attr('fill', '#73C2FB') //#73C2FB
            .attr('class', 'rnode')
            .on('mouseover', (d) => {
              that.fade(d)
            })
            .on('mouseout', (d) => {
              that.fadeOut()
            })
            .attr("rx", 6)
            .attr("ry", 6)
        u.exit().remove()

        u = d3.select('.nodes')
          .selectAll('image')
          .data(filteredNodes.filter((d) => {return d.Type === 'Team'}))

        u.enter()
          .append('image')
            .merge(u)
            .attr('xlink:href', (d) => {
              return 'https://static.nfl.com/static/site/img/logos/svg/teams/' + d.Name + '.svg'
            })
            .attr('width', 70)
            .attr('height', 70)
            .attr('x', (d) => {return d.x - 70 / 2})
            .attr('y', (d) => {return d.y - 70 / 2})
            .on('mouseover', (d) => {
              that.fade(d)
            })
            .on('mouseout', (d) => {
              that.fadeOut()
            })

        u.exit().remove()

        u = d3.select('.nodes')
          .selectAll('text')
          .data(filteredNodes.filter((d) => {return d.Type === 'Player'}))

        u.enter()
          .append('text')
            .merge(u)
            .text((d) => {
              if (d.Value > 3000000) {
                return d.Pos.replace(/[0-9]/g, '');
              } else {
                return ''
              }
            })
            .attr('class', 'playerText')
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
              that.fade(d)
            })
            .on('mouseout', (d) => {
              tooltip
                .style('opacity', 0)
              that.fadeOut()
            })
        u.exit().remove()
      }
    }
  }
</script>

<style>
line {
  stroke-width: 5px;
}
text {
  fill: #666;
  font-family: "Helvetica Neue", Helvetica, sans-serif;
  font-size: 12.5px
}
.playerText {
  text-anchor: middle !important;
  font-size: 18px !important;
}
.legendText {
  text-anchor: left !important;
  font-size: 14px !important;
}
.filterText {
  font-size: 14px !important;
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
