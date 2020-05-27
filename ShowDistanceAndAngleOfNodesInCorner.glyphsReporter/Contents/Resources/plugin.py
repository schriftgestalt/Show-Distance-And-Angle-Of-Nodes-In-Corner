# encoding: utf-8
from __future__ import division, print_function, unicode_literals

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# --> let me know if you have ideas for improving
# --> Mark Froemberg aka DeutschMark @ GitHub
# --> www.markfromberg.com
#
# - Note:
# 		+ About Relative/Absolute/Shortest angle: https://forum.glyphsapp.com/t/show-distance-and-angle/8176/17
#
# - ToDo
#	-
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSString
from AppKit import NSColor, NSBezierPath
import math
import traceback

@objc.python_method
def UnitVectorFromTo(B, A):
	A.x -= B.x
	A.y -= B.y
	Length = math.sqrt((A.x * A.x) + (A.y * A.y))
	A.x /= Length
	A.y /= Length
	return A

COLOR = 0, .6, 1, 0.75

class ShowDistanceAndAngleInCorner( ReporterPlugin ):

	@objc.python_method
	def settings(self):
		try:
			self.menuName = Glyphs.localize({
				'en': "Distance & Angle in Corner",
				'de': 'Abstand & Winkel in der Ecke',
				'fr': 'distance & angle dans un coin',
				'es': 'distancia & angulo en esquina',
			})
			
			# print(self.menuName, "Version 1.0.5")
			self.thisMenuTitle = {"name": u"%s:" % self.menuName, "action": None }
			self.vID = "com.markfromberg.ShowDistanceAndAngleInCorner" # vendorID

			self.angleAbsolute = True
			# if not self.LoadPreferences( ):
			# 	print("Error: Could not load preferences. Will resort to defaults.")

			# self.angleStyles = {
			# 	"True" : u"= Relative Angle",
			# 	"False" : u"= Shortest Angle", # Absolute = % 360
			# }

			# self.generalContextMenus = [
			# 	self.thisMenuTitle,
			# 	{"name": u"%s" % self.angleStyles[str(self.angleAbsolute)], "action": self.toggleAngleStyle },
			# ]
		except:
			print(traceback.format_exc())

	# @objc.python_method
	# def toggleAngleStyle(self):
	# 	try:
	# 		self.angleAbsolute = not self.angleAbsolute
	# 		self.generalContextMenus = [
	# 			self.thisMenuTitle,
	# 			{"name": u"%s" % self.angleStyles[str(self.angleAbsolute)], "action": self.toggleAngleStyle },
	# 		]
	# 		self.RefreshView()
	# 		self.SavePreferences()
	# 	except:
	# 		print(traceback.format_exc())

	# @objc.python_method
	# def SavePreferences( self ):
	# 	try:
	# 		Glyphs.defaults[ "%s.angleStyle" % self.vID ] = self.angleAbsolute # self.w.hTarget.get()
	# 	except:
	# 		print(traceback.format_exc())

	# @objc.python_method
	# def LoadPreferences( self ):
	# 	try:
	# 		Glyphs.registerDefault( "%s.angleStyle" % self.vID, True ) # Default
	# 		try:
	# 			self.angleAbsolute = Glyphs.defaults[ "%s.angleStyle" % self.vID ]
	# 		except:
	# 			return False

	# 		return True
	# 	except:
	# 		print(traceback.format_exc())

	@objc.python_method
	def foregroundInViewCoords(self, layer=None):
		if not layer:
			layer = self.controller.activeLayer()
		if layer:
			try:
				self.drawNodeDistanceText( layer )
			except:
				print(traceback.format_exc())

	@objc.python_method
	def background(self, layer):
		try:
			try:
				selection = layer.selection
			except:
				selection = layer.selection()
			if len(selection) == 2:
				if hasattr(selection[0], "component"):
					x1, y1 = selection[0].bounds.origin.x + selection[0].bounds.size.width/2, selection[0].bounds.origin.y + selection[0].bounds.size.height/2
				else:
					x1, y1 = selection[0].x, selection[0].y
				if hasattr(selection[1], "component"):
					x2, y2 = selection[1].bounds.origin.x + selection[1].bounds.size.width/2, selection[1].bounds.origin.y + selection[1].bounds.size.height/2
				else:
					x2, y2 = selection[1].x, selection[1].y

				toolEventHandler = self.controller.view().window().windowController().toolEventHandler()

				toolIsTextTool = toolEventHandler.className() == "GlyphsToolText"
				toolIsToolHand = toolEventHandler.className() == "GlyphsToolHand"

				currentController = self.controller.view().window().windowController()
				if currentController:
				    if not toolIsTextTool and not toolIsToolHand:
						self.drawLine(x1, y1, x2, y2)
		except:
			print(traceback.format_exc())

		# 	if len(selection) == 2:
		# 		x1, y1 = selection[0].x, selection[0].y
		# 		x2, y2 = selection[1].x, selection[1].y
		# 		self.drawLine(x1, y1, x2, y2)
		# except:
		# 	print(traceback.format_exc())

	# @objc.python_method
	# def drawCoveringBadge(self, x, y, width, height, radius):
	# 	try:
	# 		myPath = NSBezierPath.alloc().init()
	# 		NSColor.colorWithCalibratedRed_green_blue_alpha_( *COLOR ).set()
	# 		myRect = NSRect( ( x, y ), ( width, height ) )
	# 		thisPath = NSBezierPath.bezierPathWithRoundedRect_cornerRadius_( myRect, radius )
	# 		myPath.appendBezierPath_( thisPath )
	# 		myPath.fill()
	# 	except:
	# 		print(traceback.format_exc())

	@objc.python_method
	def drawLine(self, x1, y1, x2, y2, strokeWidth=1):
		try:
			myPath = NSBezierPath.bezierPath()
			myPath.moveToPoint_( (x1, y1) )
			myPath.lineToPoint_( (x2, y2) )
			myPath.setLineWidth_( strokeWidth/self.getScale() )
			selectionColor = 0, 0, 0.5, 0.2
			NSColor.colorWithCalibratedRed_green_blue_alpha_( *selectionColor ).set()
			myPath.stroke()
		except:
			print(traceback.format_exc())

	@objc.python_method
	def drawNodeDistanceText( self, layer ):
		if layer is None:
			return
		try:
			try:
				selection = layer.selection
			except:
				selection = layer.selection()
			if len(selection) == 2:
				x1, y1 = selection[0].x, selection[0].y
				x2, y2 = selection[1].x, selection[1].y

				# Fix order
				if x1 > x2:
					x2, x1 = x1, x2
					y2, y1 = y1, y2

				t = 0.5 # MIDLLE
				xAverage = x1 + (x2-x1) * t
				yAverage = y1 + (y2-y1) * t
				dist = math.hypot(x2 - x1, y2 - y1)
				

				# Angle
				#======
				# print x2 >= x1 or y2 >= y1
				switch = (x1, y1) >= (x2, y2)

				
				if switch == True and self.angleAbsolute == False:
					dx, dy = x1 - x2, y1 - y2
					#print "switch"
				else:
					dx, dy = x2 - x1, y2 - y1
				rads = math.atan2( dy, dx )
				degs = math.degrees( rads )

				dx2, dy2 = x1 - x2, y1 - y2
				rads2 = math.atan2( dy2, dx2 )
				degs2 = math.degrees( rads2 )

				degs_ = 90-degs
				degs2_ = 90-degs2

				if self.angleAbsolute == True:
					degs = degs % 180 # Not using 360 here. same angles will have the same number, no matter the path direction of this segment
				if self.angleAbsolute == False:
					degs = abs(degs) % 90
				
				scale = self.getScale()
				# string = NSString.stringWithString_(u"%s\n%s°" % ( round(dist, 1), round(degs, 1) ))

				string = u"𝙸 %s\n∠: %s° / %s° | ⩗: %s° / %s°" % ( round(dist, 1), round(degs, 1), round(degs2, 1), round(degs_, 1), round(degs2_, 1) )
				
				self.drawText( string )
		except:
			print(traceback.format_exc())
			pass

	@objc.python_method
	def drawText( self, text, fontColor=NSColor.whiteColor() ):
		try:
			fontSize = Glyphs.defaults["com.mekkablue.ShowDistanceAndAngle3.fontSize"]

			fontAttributes = { 
				#NSFontAttributeName: NSFont.labelFontOfSize_(10.0),
				NSFontAttributeName: NSFont.monospacedDigitSystemFontOfSize_weight_(fontSize,0.0),
				NSForegroundColorAttributeName: NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.5, 0.5, 0.5, 1 )
			}
			
			displayText = NSAttributedString.alloc().initWithString_attributes_(text, fontAttributes)
			textAlignment = 0 
			upperLeftCorner = NSPoint( self.controller.viewPort.origin.x + 5 , self.controller.viewPort.origin.y + self.controller.viewPort.size.height - 32)
			displayText.drawAtPoint_alignment_(upperLeftCorner, textAlignment)
		except:
			print(traceback.format_exc())

	def needsExtraMainOutlineDrawingForInactiveLayer_( self, layer ):
		return True

	@objc.python_method
	def RefreshView(self):
		try:
			Glyphs = NSApplication.sharedApplication()
			currentTabView = Glyphs.font.currentTab
			if currentTabView:
				currentTabView.graphicView().setNeedsDisplay_(True)
		except:
			pass

	@objc.python_method
	def getScale( self ):
		try:
			return self._scale
		except:
			return 1 # Attention, just for debugging!

	@objc.python_method
	def logToConsole( self, message ):
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
