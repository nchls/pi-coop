import React from 'react';
import { RecoilRoot } from 'recoil';

import './app.scss';
import Door from '../door/door';


const App = () => {
	return (
		<RecoilRoot>
			<main>
				<Door />
			</main>
		</RecoilRoot>
	);
};

export default App;