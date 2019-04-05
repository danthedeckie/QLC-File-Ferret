'''
    XML Snippets for building valid QXW files for testing.

    Structure:

    header
      engine_header
        <Any Fixtures you want to use>
        <Any Functions you want to use>
      engine_footer
      virtual_console (default is empty_virtual_console)
      simple_desk (default is empty_simple_desk)
    footer
'''

header = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Workspace>
<Workspace xmlns="http://www.qlcplus.org/Workspace" CurrentWindow="FixtureManager">
 <Creator>
  <Name>Q Light Controller Plus</Name>
  <Version>4.12.0</Version>
  <Author>daniel.fairhead</Author>
 </Creator>
 '''
engine_header = '''<Engine>
  <InputOutputMap>
   <Universe Name="Universe 1" ID="0">
    <Output Plugin="E1.31" Line="1">
     <PluginParameters UniverseChannels="363"/>
    </Output>
   </Universe>
   <Universe Name="Universe 2" ID="1"/>
   <Universe Name="Universe 3" ID="2"/>
   <Universe Name="Universe 4" ID="3"/>
  </InputOutputMap>
'''

engine_footer = '</Engine>'

footer = '''
</Workspace>
'''

empty_virtual_console = '''
<VirtualConsole>
  <Frame Caption="">
   <Appearance>
    <FrameStyle>None</FrameStyle>
    <ForegroundColor>Default</ForegroundColor>
    <BackgroundColor>Default</BackgroundColor>
    <BackgroundImage>None</BackgroundImage>
    <Font>Default</Font>
   </Appearance>
  </Frame>
  <Properties>
   <Size Width="1920" Height="1080"/>
   <GrandMaster ChannelMode="Intensity" ValueMode="Reduce" SliderMode="Normal"/>
  </Properties>
 </VirtualConsole>
'''

empty_simple_desk = '''
 <SimpleDesk>
  <Engine/>
 </SimpleDesk>
'''

def generic_fixture(uid, address, channels=1, universe=0, name=None):
    return '''
   <Fixture>
   <Manufacturer>Generic</Manufacturer>
   <Model>Generic</Model>
   <Mode>1 Channel</Mode>
   <ID>{uid}</ID>
   <Name>{name}</Name>
   <Universe>{universe}</Universe>
   <Address>{address}</Address>
   <Channels>{channels}</Channels>
  </Fixture>
    '''.format(uid=uid, address=address, universe=universe, channels=channels,
               name=name or 'Dimmer %i' % uid)

def function_scene(uid, name, path=""):
    return '''<Function ID="{uid}" Type="Scene" Name="{name}" Path="{path}">
   <Speed FadeIn="0" FadeOut="0" Duration="0"/>
  </Function>'''.format(uid=uid, name=name, path=path)
