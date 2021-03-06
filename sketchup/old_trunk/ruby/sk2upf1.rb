#!/usr/bin/env ruby
#
#  Created by santosh on 2006-09-12.
#  Copyright (c) 2006. All rights reserved.

# dumps the some sketchup geometry data to a file
# for each face it dumps the points3d

require "Sketchup.rb" #Make sure this ruby file is loaded
model=Sketchup.active_model             # point to the active model

selection_set = model.active_entities # get the all entities

aFile = File.new("/Users/santosh/Documents/coolshadowprojects/sketchupstuff/ruby/a.txt", 'w')


selection_set.each {|entity|
  if entity.class == Sketchup::Face
    face = entity
    allloops = face.loops
    allloops.each {|lp|
      if lp.outer?
        snippet3 = sprintf('%s outer', lp )
        aFile.puts('--------------------')
        puts snippet3
        allvertex = lp.vertices
        allvertex.each{|vert|
          pts = vert.position.to_a
          snippet4 = sprintf('%s, %s, %s', pts[0], pts[1], pts[2] )
          puts snippet4
          aFile.puts(snippet4)
          }
      else
        snippet3 = sprintf('%s inner', lp )
        puts snippet3
      end
      }
  end
  }

aFile.close()