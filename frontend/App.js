import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Home from './pages/Home';
import Details from './pages/Details';

const Stack = createNativeStackNavigator();

export default function App() {
  
  return (
    <NavigationContainer linking={{enabled: true}}>
      <Stack.Navigator screenOptions={{headerShown: false}}>
        <Stack.Screen
          name="home"
          component={Home}
        />
        <Stack.Screen name="details" component={Details} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
