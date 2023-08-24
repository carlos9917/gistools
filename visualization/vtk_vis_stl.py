#!/usr/bin/env python
import vtk
import sys

ifile = sys.argv[1]
reader = vtk.vtkSTLReader()
reader.SetFileName(ifile)
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())
actor = vtk.vtkActor()
actor.SetMapper(mapper)
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1) # Background color

renderWindow.Render()
renderWindowInteractor.Start()
