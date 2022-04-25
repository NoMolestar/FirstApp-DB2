import { useIsFocused } from '@react-navigation/native';
import { useEffect, useState } from 'react';
import { FlatList } from 'react-native';
import Product from '../components/Product';

const Home = ({ navigation }) => {
    const [data, setData] = useState([]);
    const isFocused = useIsFocused();

    const getDataFromAPI = () => {
      return fetch('http://localhost:5000/select')
        .then((response) => response.json())
        .then((json) => {
          return json;
        })
        .catch((error) => {
          console.error(error);
        });
    };
  
    useEffect(() => {
      getDataFromAPI().then((data) => setData(data));
    }, [isFocused]);

    return (
      <FlatList 
        data={data}
        renderItem={({item}) => <Product id={item.id} name={item.name} nav={navigation}/>}
      />
    );
};

export default Home;