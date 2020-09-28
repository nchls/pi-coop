import React from 'react';
import { RecoilRoot } from 'recoil';

import './app.scss';
import Door from '../door/door';
import Environment from '../environment/environment';
import Pi from '../pi/pi';


const App = () => {
	return (
		<RecoilRoot>
			<main className="panels">
				<div className="panel is-primary door">
					<Door />
				</div>
				<div className="panel is-link pi">
					<Pi />
				</div>
				<div className="panel is-warning environment">
					<Environment />
				</div>
			</main>
		</RecoilRoot>
	);
};

export default App;