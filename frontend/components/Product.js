import { Text, View } from 'react-native';
import { TouchableHighlight } from 'react-native-gesture-handler';
import styles from '../styles/Styles';

const Product = (props) => {
    
    const handleClick = () => {
        props.nav.navigate("details", {id: props.id});
    }

    const onUpdate = () => {
        props.nav.navigate("info", {id: props.id});
    };

    return (
        <View style={styles.productContainer} onPress={handleClick}>
            <TouchableHighlight 
                onPress={handleClick}
                underlayColor="white"
                style={styles.TouchableHighlight}
            >
                <Text style={styles.item}>{props.id}: {props.name}</Text>
            </TouchableHighlight>
            <Button onPress={onUpdate} title="Update"/>
        </View>
    );
}

export default Product;