import React, { useState } from 'react';
import { atom, useRecoilValue } from 'recoil';

import { useAPIPoll } from '../app/utils';
import './camera.scss';


export const cameraState = atom({
	key: 'camera',
	default: {
		fetched: false,
		error: undefined,
		serviceStarted: false
	}
});

const Camera = () => {
	useAPIPoll(cameraState, '/camera/ping', 10000);
	const [isLoading, setIsLoading] = useState(true);
	const camera = useRecoilValue(cameraState);

	return (
		<div className="panel is-info camera">
			<div className="panel-heading">Cameras</div>
			<div className="panel-block inside">
				<div className="video-container">
					{ isLoading && <div className="loader"/> }
					<img 
						src={`${window.location.origin}:8081?q=${Date.now()}`} 
						onLoad={() => { 
							if (isLoading) { 
								setIsLoading(false)
							}
						}}
						onError={(err) => {
							if (!isLoading) {
								console.error(err);
								setIsLoading(true);
							}
						}}
						alt="Inside coop camera"
					/>
					<img 
						src={`${window.location.origin}:8082?q=${Date.now()}`} 
						onLoad={() => { 
							if (isLoading) { 
								setIsLoading(false)
							}
						}}
						onError={(err) => {
							if (!isLoading) {
								console.error(err);
								setIsLoading(true);
							}
						}}
						alt="Outside coop camera"
					/>
				</div>
			</div>
		</div>
	);
};

export default Camera;
