import React from 'react';
import { RecoilRoot } from 'recoil';

import './app.scss';
import Door from '../door/door';
import Environment from '../environment/environment';
import Faults from '../faults/faults';
import Pi from '../pi/pi';
import Camera from '../camera/camera';


const App = () => {
	return (
		<RecoilRoot>
			<main className="panels">
				<Faults />
				<Door />
				<Pi />
				<Environment />
				<Camera />
			</main>
		</RecoilRoot>
	);
};

export default App;